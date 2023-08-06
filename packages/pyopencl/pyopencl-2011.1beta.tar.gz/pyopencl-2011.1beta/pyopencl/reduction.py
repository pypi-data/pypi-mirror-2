"""Computation of reductions on vectors."""

from __future__ import division

__copyright__ = "Copyright (C) 2010 Andreas Kloeckner"

__license__ = """
Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Based on code/ideas by Mark Harris <mharris@nvidia.com>.
None of the original source code remains.
"""




import pyopencl as cl
from pyopencl.tools import (
        context_dependent_memoize,
        dtype_to_ctype)
from pytools import memoize_method
import numpy as np




KERNEL = """
    #define GROUP_SIZE ${group_size}
    #define READ_AND_MAP(i) (${map_expr})
    #define REDUCE(a, b) (${reduce_expr})

    % if double_support:
        #pragma OPENCL EXTENSION cl_khr_fp64: enable
    % endif

    typedef ${out_type} out_type;

    ${preamble}

    __kernel void ${name}(
      __global out_type *out, ${arguments},
      unsigned int seq_count, unsigned int n)
    {
        __local out_type ldata[GROUP_SIZE];

        unsigned int lid = get_local_id(0);

        unsigned int i = get_group_id(0)*GROUP_SIZE*seq_count + lid;

        out_type acc = ${neutral};
        for (unsigned s = 0; s < seq_count; ++s)
        {
          if (i >= n)
            break;
          acc = REDUCE(acc, READ_AND_MAP(i));

          i += GROUP_SIZE;
        }

        ldata[lid] = acc;

        <%
          cur_size = group_size
        %>

        % while cur_size > no_sync_size:
            barrier(CLK_LOCAL_MEM_FENCE);

            <%
            new_size = cur_size // 2
            assert new_size * 2 == cur_size
            %>

            if (lid < ${new_size})
            {
                ldata[lid] = REDUCE(
                  ldata[lid],
                  ldata[lid + ${new_size}]);
            }

            <% cur_size = new_size %>

        % endwhile

        % if cur_size > 1:
            ## we need to synchronize one last time for entry into the
            ## no-sync region.

            barrier(CLK_LOCAL_MEM_FENCE);

            if (lid < ${no_sync_size})
            {
                __local volatile out_type *lvdata = ldata;
                % while cur_size > 1:
                    <%
                    new_size = cur_size // 2
                    assert new_size * 2 == cur_size
                    %>

                    lvdata[lid] = REDUCE(
                      lvdata[lid],
                      lvdata[lid + ${new_size}]);

                    <% cur_size = new_size %>

                % endwhile

            }
        % endif

        if (lid == 0) out[get_group_id(0)] = ldata[0];
    }
    """




def  get_reduction_source(
         ctx, out_type, out_type_size,
         neutral, reduce_expr, map_expr, arguments,
         name="reduce_kernel", preamble="",
         device=None, max_group_size=None):

    if device is not None:
        devices = [device]
    else:
        devices = ctx.devices

    # {{{ compute group size

    def get_dev_group_size(device):
        return min(
                device.max_work_group_size,
                (device.local_mem_size + out_type_size - 1)
                // out_type_size)

    group_size = min(
            get_dev_group_size(dev) for dev in devices)

    if max_group_size is not None:
        group_size = min(max_group_size, group_size)

    # }}}

    # {{{ compute synchronization-less group size

    def get_dev_no_sync_size(device):
        try:
            return device.warp_size_nv
        except:
            if "nvidida" in device.vendor.lower():
                from warnings import warn
                warn("Reduction might be unnecessarily slow: "
                        "can't query warp size on Nvidia device")
            return 1

    no_sync_size = min(get_dev_no_sync_size(dev) for dev in devices)

    # }}}

    from mako.template import Template
    from pytools import all
    from pyopencl.tools import has_double_support
    src = Template(KERNEL).render(
        out_type=out_type,
        arguments=arguments,
        group_size=group_size,
        no_sync_size=no_sync_size,
        neutral=neutral,
        reduce_expr=reduce_expr,
        map_expr=map_expr,
        name=name,
        preamble=preamble,
        double_support=all(
            has_double_support(dev) for dev in devices)
        )

    from pytools import Record
    class ReductionInfo(Record):
        pass

    return ReductionInfo(
            context=ctx,
            source=src,
            group_size=group_size)




def get_reduction_kernel(
         ctx, out_type, out_type_size,
         neutral, reduce_expr, map_expr=None, arguments=None,
         name="reduce_kernel", preamble="",
         device=None, options="", max_group_size=None):
    if map_expr is None:
        map_expr = "in[i]"

    if arguments is None:
        arguments = "__global const %s *in" % out_type

    inf = get_reduction_source(
            ctx, out_type, out_type_size,
            neutral, reduce_expr, map_expr, arguments,
            name, preamble, device, max_group_size)

    inf.program = cl.Program(ctx, inf.source)
    inf.program.build()
    inf.kernel = getattr(inf.program, name)

    from pyopencl.tools import parse_c_arg, ScalarArg

    inf.arg_types = [parse_c_arg(arg) for arg in arguments.split(",")]
    scalar_arg_dtypes = [None]
    for arg_type in inf.arg_types:
        if isinstance(arg_type, ScalarArg):
            scalar_arg_dtypes.append(arg_type.dtype)
        else:
            scalar_arg_dtypes.append(None)
    scalar_arg_dtypes.extend([np.uint32]*2)

    inf.kernel.set_scalar_arg_dtypes(scalar_arg_dtypes)

    return inf




class ReductionKernel:
    def __init__(self, ctx, dtype_out,
            neutral, reduce_expr, map_expr=None, arguments=None,
            name="reduce_kernel", options="", preamble=""):

        self.dtype_out = dtype_out

        self.stage_1_inf = get_reduction_kernel(ctx,
                dtype_to_ctype(dtype_out), dtype_out.itemsize,
                neutral, reduce_expr, map_expr, arguments,
                name=name+"_stage1", options=options, preamble=preamble)

        # stage 2 has only one input and no map expression
        self.stage_2_inf = get_reduction_kernel(ctx,
                dtype_to_ctype(dtype_out), dtype_out.itemsize,
                neutral, reduce_expr,
                name=name+"_stage2", options=options, preamble=preamble)

        from pytools import any
        from pyopencl.tools import VectorArg
        assert any(
                isinstance(arg_tp, VectorArg)
                for arg_tp in self.stage_1_inf.arg_types), \
                "ReductionKernel can only be used with functions that have at least one " \
                "vector argument"

    def __call__(self, *args, **kwargs):
        MAX_GROUP_COUNT = 1024
        SMALL_SEQ_COUNT = 4

        from pyopencl.array import empty

        stage_inf = self.stage_1_inf

        queue = kwargs.pop("queue", None)

        if kwargs:
            raise TypeError("invalid keyword argument to reduction kernel")

        while True:
            invocation_args = []
            vectors = []

            from pyopencl.tools import VectorArg
            for arg, arg_tp in zip(args, stage_inf.arg_types):
                if isinstance(arg_tp, VectorArg):
                    vectors.append(arg)
                    invocation_args.append(arg.data)
                else:
                    invocation_args.append(arg)

            repr_vec = vectors[0]
            sz = repr_vec.size

            if queue is not None:
                use_queue = queue
            else:
                use_queue = repr_vec.queue

            if sz <= stage_inf.group_size*SMALL_SEQ_COUNT*MAX_GROUP_COUNT:
                total_group_size = SMALL_SEQ_COUNT*stage_inf.group_size
                group_count = (sz + total_group_size - 1) // total_group_size
                seq_count = SMALL_SEQ_COUNT
            else:
                group_count = MAX_GROUP_COUNT
                macrogroup_size = group_count*stage_inf.group_size
                seq_count = (sz + macrogroup_size - 1) // macrogroup_size

            if group_count == 1:
                result = empty(stage_inf.context,
                        (), self.dtype_out,
                        allocator=repr_vec.allocator,
                        queue=use_queue)
            else:
                result = empty(stage_inf.context,
                        (group_count,), self.dtype_out,
                        allocator=repr_vec.allocator,
                        queue=use_queue)

            #print group_count, seq_count, stage_inf.group_size
            stage_inf.kernel(
                    use_queue,
                    (group_count*stage_inf.group_size,),
                    (stage_inf.group_size,),
                    *([result.data]+invocation_args+[seq_count, sz]))

            if group_count == 1:
                return result
            else:
                stage_inf = self.stage_2_inf
                args = [result]




@context_dependent_memoize
def get_sum_kernel(ctx, dtype_out, dtype_in):
    if dtype_out is None:
        dtype_out = dtype_in

    return ReductionKernel(ctx, dtype_out, "0", "a+b",
            arguments="__global const %(tp)s *in"
            % {"tp": dtype_to_ctype(dtype_in)})




@context_dependent_memoize
def get_dot_kernel(ctx, dtype_out, dtype_a=None, dtype_b=None):
    if dtype_out is None:
        dtype_out = dtype_a

    if dtype_b is None:
        if dtype_a is None:
            dtype_b = dtype_out
        else:
            dtype_b = dtype_a

    if dtype_a is None:
        dtype_a = dtype_out

    return ReductionKernel(ctx, dtype_out, neutral="0",
            reduce_expr="a+b", map_expr="a[i]*b[i]",
            arguments=
            "__global const %(tp_a)s *a, "
            "__global const %(tp_b)s *b" % {
                "tp_a": dtype_to_ctype(dtype_a),
                "tp_b": dtype_to_ctype(dtype_b),
                })




@context_dependent_memoize
def get_subset_dot_kernel(ctx, dtype_out, dtype_a=None, dtype_b=None):
    if dtype_out is None:
        dtype_out = dtype_a

    if dtype_b is None:
        if dtype_a is None:
            dtype_b = dtype_out
        else:
            dtype_b = dtype_a

    if dtype_a is None:
        dtype_a = dtype_out

    # important: lookup_tbl must be first--it controls the length
    return ReductionKernel(ctx, dtype_out, neutral="0",
            reduce_expr="a+b", map_expr="a[lookup_tbl[i]]*b[lookup_tbl[i]]",
            arguments=
            "__global const unsigned int *lookup_tbl, "
            "__global const %(tp_a)s *a, "
            "__global const %(tp_b)s *b" % {
            "tp_a": dtype_to_ctype(dtype_a),
            "tp_b": dtype_to_ctype(dtype_b),
            })




def get_minmax_neutral(what, dtype):
    dtype = np.dtype(dtype)
    if issubclass(dtype.type, np.inexact):
        if what == "min":
            return "MY_INFINITY"
        elif what == "max":
            return "-MY_INFINITY"
        else:
            raise ValueError("what is not min or max.")
    else:
        if what == "min":
            return str(np.iinfo(dtype).max)
        elif what == "max":
            return str(np.iinfo(dtype).min)
        else:
            raise ValueError("what is not min or max.")




@context_dependent_memoize
def get_minmax_kernel(ctx, what, dtype):
    if dtype.kind == "f":
        reduce_expr = "f%s(a,b)" % what
    elif dtype.kind in "iu":
        reduce_expr = "%s(a,b)" % what
    else:
        raise TypeError("unsupported dtype specified")

    return ReductionKernel(ctx, dtype,
            neutral=get_minmax_neutral(what, dtype),
            reduce_expr="%(reduce_expr)s" % {"reduce_expr": reduce_expr},
            arguments="__global const %(tp)s *in" % {
                "tp": dtype_to_ctype(dtype),
                }, preamble="#define MY_INFINITY (1./0)")




@context_dependent_memoize
def get_subset_minmax_kernel(ctx, what, dtype):
    if dtype.kind == "f":
        reduce_expr = "f%s(a,b)" % what
    elif dtype.kind in "iu":
        reduce_expr = "%s(a,b)" % what
    else:
        raise TypeError("unsupported dtype specified")

    return ReductionKernel(ctx, dtype,
            neutral=get_minmax_neutral(what, dtype),
            reduce_expr="%(reduce_expr)s" % {"reduce_expr": reduce_expr},
            map_expr="in[lookup_tbl[i]]",
            arguments=
            "__global const unsigned int *lookup_tbl, "
            "__global const %(tp)s *in"  % {
            "tp": dtype_to_ctype(dtype),
            }, preamble="#define MY_INFINITY (1./0)")
