from __future__ import division
import numpy
import numpy.linalg as la
import pytools.test




def have_cl():
    try:
        import pyopencl
        return True
    except:
        return False



if have_cl():
    import pyopencl as cl
    from pyopencl.tools import pytest_generate_tests_for_pyopencl \
            as pytest_generate_tests




class TestCL:
    disabled = not have_cl()

    @pytools.test.mark_test.opencl
    def test_get_info(self, platform, device):
        failure_count = [0]

        CRASH_QUIRKS = [
                (("NVIDIA Corporation", "NVIDIA CUDA",
                    "OpenCL 1.0 CUDA 3.0.1"),
                    [
                    (cl.Event, cl.event_info.COMMAND_QUEUE),
                    ]),
                ]
        QUIRKS = []

        plat_quirk_key = (
                platform.vendor,
                platform.name,
                platform.version)

        def find_quirk(quirk_list, cl_obj, info):
            for entry_plat_key, quirks in quirk_list:
                if entry_plat_key == plat_quirk_key:
                    for quirk_cls, quirk_info in quirks:
                        if (isinstance(cl_obj, quirk_cls)
                                and quirk_info == info):
                            return True

            return False

        def do_test(cl_obj, info_cls, func=None, try_attr_form=True):
            if func is None:
                def func(info):
                    cl_obj.get_info(info)

            for info_name in dir(info_cls):
                if not info_name.startswith("_") and info_name != "to_string":
                    info = getattr(info_cls, info_name)

                    if find_quirk(CRASH_QUIRKS, cl_obj, info):
                        print "not executing get_info", type(cl_obj), info_name
                        print "(known crash quirk for %s)" % platform.name
                        continue

                    try:
                        func(info)
                    except:
                        msg = "failed get_info", type(cl_obj), info_name

                        if find_quirk(QUIRKS, cl_obj, info):
                            msg += ("(known quirk for %s)" % platform.name)
                        else:
                            failure_count[0] += 1

                    if try_attr_form:
                        try:
                            getattr(cl_obj, info_name.lower())
                        except:
                            print "failed attr-based get_info", type(cl_obj), info_name

                            if find_quirk(QUIRKS, cl_obj, info):
                                print "(known quirk for %s)" % platform.name
                            else:
                                failure_count[0] += 1

        do_test(platform, cl.platform_info)

        do_test(device, cl.device_info)

        ctx = cl.Context([device])
        do_test(ctx, cl.context_info)

        props = 0
        if (device.queue_properties
                & cl.command_queue_properties.PROFILING_ENABLE):
            profiling = True
            props = cl.command_queue_properties.PROFILING_ENABLE
        queue = cl.CommandQueue(ctx,
                properties=props)
        do_test(queue, cl.command_queue_info)

        prg = cl.Program(ctx, """
            __kernel void sum(__global float *a)
            { a[get_global_id(0)] *= 2; }
            """).build()
        do_test(prg, cl.program_info)
        do_test(prg, cl.program_build_info,
                lambda info: prg.get_build_info(device, info),
                try_attr_form=False)

        cl.unload_compiler() # just for the heck of it

        mf = cl.mem_flags
        n = 2000
        a_buf = cl.Buffer(ctx, 0, n*4)

        do_test(a_buf, cl.mem_info)

        kernel = prg.sum
        do_test(kernel, cl.kernel_info)

        evt = kernel(queue, (n,), None, a_buf)
        do_test(evt, cl.event_info)

        if profiling:
            evt.wait()
            do_test(evt, cl.profiling_info,
                    lambda info: evt.get_profiling_info(info),
                    try_attr_form=False)

        if device.image_support:
            smp = cl.Sampler(ctx, True,
                    cl.addressing_mode.CLAMP,
                    cl.filter_mode.NEAREST)
            do_test(smp, cl.sampler_info)

            img_format = cl.get_supported_image_formats(
                    ctx, cl.mem_flags.READ_ONLY, cl.mem_object_type.IMAGE2D)[0]

            img = cl.Image(ctx, cl.mem_flags.READ_ONLY, img_format, (128, 256))
            assert img.shape == (128, 256)

            img.depth
            img.image.depth
            do_test(img, cl.image_info,
                    lambda info: img.get_image_info(info))

        if failure_count[0]:
            raise RuntimeError(
                    "get_info testing had %d errors "
                    "(If you compiled against OpenCL 1.1 but are testing a 1.0 "
                    "implementation, you can safely ignore this.)"
                    % failure_count[0])

    @pytools.test.mark_test.opencl
    def test_invalid_kernel_names_cause_failures(self):
        for platform in cl.get_platforms():
            for device in platform.get_devices():
                ctx = cl.Context([device])
                prg = cl.Program(ctx, """
                    __kernel void sum(__global float *a)
                    { a[get_global_id(0)] *= 2; }
                    """).build()

                try:
                    prg.sam
                    raise RuntimeError("invalid kernel name did not cause error")
                except AttributeError:
                    pass

    @pytools.test.mark_test.opencl
    def test_image_format_constructor(self):
        # doesn't need image support to succeed
        iform = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.FLOAT)

        assert iform.channel_order == cl.channel_order.RGBA
        assert iform.channel_data_type == cl.channel_type.FLOAT
        assert not iform.__dict__

    @pytools.test.mark_test.opencl
    def test_nonempty_supported_image_formats(self, device, ctx_getter):
        context = ctx_getter()

        if device.image_support:
            assert len(cl.get_supported_image_formats(
                    context, cl.mem_flags.READ_ONLY, cl.mem_object_type.IMAGE2D)) > 0
        else:
            from py.test import skip
            skip("images not supported on %s" % device.name)

    @pytools.test.mark_test.opencl
    def test_that_python_args_fail(self, ctx_getter):
        context = ctx_getter()

        prg = cl.Program(context, """
            __kernel void mult(__global float *a, float b, int c)
            { a[get_global_id(0)] *= (b+c); }
            """).build()

        a = numpy.random.rand(50000)
        queue = cl.CommandQueue(context)
        mf = cl.mem_flags
        a_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=a)

        try:
            prg.mult(queue, a.shape, None, a_buf, 2, 3)
            assert False, "PyOpenCL should not accept bare Python types as arguments"
        except cl.LogicError:
            pass

        try:
            prg.mult(queue, a.shape, None, a_buf, float(2), 3)
            assert False, "PyOpenCL should not accept bare Python types as arguments"
        except cl.LogicError:
            pass

        prg.mult(queue, a.shape, None, a_buf, numpy.float32(2), numpy.int32(3))

        a_result = numpy.empty_like(a)
        cl.enqueue_read_buffer(queue, a_buf, a_result).wait()

    @pytools.test.mark_test.opencl
    def test_image_2d(self, device, ctx_getter):
        context = ctx_getter()

        if not device.image_support:
            from py.test import skip
            skip("images not supported on %s" % device)

        prg = cl.Program(context, """
            __kernel void copy_image(
              __global float4 *dest,
              __read_only image2d_t src,
              sampler_t samp,
              int width)
            {
              int x = get_global_id(0);
              int y = get_global_id(1);
              /*
              const sampler_t samp =
                CLK_NORMALIZED_COORDS_FALSE
                | CLK_ADDRESS_CLAMP
                | CLK_FILTER_NEAREST;
                */
              dest[x + width*y] = read_imagef(src, samp, (float2)(x, y));
              // dest[x + width*y] = get_image_height(src);
            }
            """).build()

        a = numpy.random.rand(1024, 1024, 4).astype(numpy.float32)
        queue = cl.CommandQueue(context)
        mf = cl.mem_flags
        a_img = cl.Image(context, mf.READ_ONLY | mf.COPY_HOST_PTR,
                cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.FLOAT),
                shape=a.shape[:2], hostbuf=a)
        a_dest = cl.Buffer(context, mf.READ_WRITE, a.nbytes)

        samp = cl.Sampler(context, False,
                cl.addressing_mode.CLAMP,
                cl.filter_mode.NEAREST)
        prg.copy_image(queue, a.shape, None, a_dest, a_img, samp, numpy.int32(a.shape[0]))

        a_result = numpy.empty_like(a)
        cl.enqueue_read_buffer(queue, a_dest, a_result, is_blocking=True)
        print a_result.dtype

        assert la.norm(a_result - a) == 0







if __name__ == "__main__":
    # make sure that import failures get reported, instead of skipping the tests.
    import pyopencl

    import sys
    if len(sys.argv) > 1:
        exec sys.argv[1]
    else:
        from py.test.cmdline import main
        main([__file__])
