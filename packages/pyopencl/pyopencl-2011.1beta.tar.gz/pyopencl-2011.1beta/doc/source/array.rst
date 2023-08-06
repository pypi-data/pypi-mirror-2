The :class:`Array` Class
========================

.. module:: pyopencl.array

.. class:: DefaultAllocator(context, flags=pyopencl.mem_flags.READ_WRITE)

    An Allocator that uses :class:`pyopencl.Buffer` with the given *flags*.

    .. method:: __call__(self, size)

.. class:: Array(context, shape, dtype, order="C", allocator=None, base=None, data=None, queue=None)

    A :class:`numpy.ndarray` work-alike that stores its data and performs its
    computations on the compute device.  *shape* and *dtype* work exactly as in
    :mod:`numpy`.  Arithmetic methods in :class:`Array` support the
    broadcasting of scalars. (e.g. `array+5`) If the

    *allocator* is a callable that, upon being called with an argument of the number
    of bytes to be allocated, returns an object that can be cast to an
    :class:`int` representing the address of the newly allocated memory.
    (See :class:`DefaultAllocator`.)

    .. attribute :: data

        The :class:`pyopencl.MemoryObject` instance created for the memory that backs
        this :class:`Array`.

    .. attribute :: shape

        The tuple of lengths of each dimension in the array.

    .. attribute :: dtype

        The :class:`numpy.dtype` of the items in the GPU array.

    .. attribute :: size

        The number of meaningful entries in the array. Can also be computed by
        multiplying up the numbers in :attr:`shape`.

    .. attribute :: mem_size

        The total number of entries, including padding, that are present in
        the array.

    .. attribute :: nbytes

        The size of the entire array in bytes. Computed as :attr:`size` times
        ``dtype.itemsize``.

    .. method :: __len__()

        Returns the size of the leading dimension of *self*.

    .. method :: set(ary, queue=None, async=False)

        Transfer the contents the :class:`numpy.ndarray` object *ary*
        onto the device.

        *ary* must have the same dtype and size (not necessarily shape) as *self*.


    .. method :: get(queue=None, ary=None, async=False)

        Transfer the contents of *self* into *ary* or a newly allocated
        :mod:`numpy.ndarray`. If *ary* is given, it must have the right
        size (not necessarily shape) and dtype.

    .. method :: __str__()
    .. method :: __repr__()

    .. method :: mul_add(self, selffac, other, otherfac, queue=None):

        Return `selffac*self + otherfac*other`.

    .. method :: __add__(other)
    .. method :: __sub__(other)
    .. method :: __iadd__(other)
    .. method :: __isub__(other)
    .. method :: __neg__(other)
    .. method :: __mul__(other)
    .. method :: __div__(other)
    .. method :: __rdiv__(other)
    .. method :: __pow__(other)

    .. method :: __abs__()

        Return a :class:`Array` containing the absolute value of each
        element of *self*.

    .. UNDOC reverse()

    .. method :: fill(scalar, queue=None)

        Fill the array with *scalar*.

    .. method :: astype(dtype, queue=None)

        Return *self*, cast to *dtype*.

Constructing :class:`Array` Instances
----------------------------------------

.. function:: to_device(context, queue, ary, allocator=None, async=False)

    Return a :class:`Array` that is an exact copy of the :class:`numpy.ndarray`
    instance *ary*.

    See :class:`Array` for the meaning of *allocator*.

.. function:: empty(context, shape, dtype, order="C", allocator=None, base=None, data=None, queue=None)

    A synonym for the :class:`Array` constructor.

.. function:: zeros(context, queue, shape, dtype, order="C", allocator=None)

    Same as :func:`empty`, but the :class:`Array` is zero-initialized before
    being returned.

.. function:: empty_like(other_ary)

    Make a new, uninitialized :class:`Array` having the same properties
    as *other_ary*.

.. function:: zeros_like(other_ary)

    Make a new, zero-initialized :class:`Array` having the same properties
    as *other_ary*.

.. function:: arange(context, queue, start, stop, step, dtype=None)

    Create a :class:`Array` filled with numbers spaced `step` apart,
    starting from `start` and ending at `stop`.

    For floating point arguments, the length of the result is
    `ceil((stop - start)/step)`.  This rule may result in the last
    element of the result being greater than `stop`.

    *dtype*, if not specified, is taken as the largest common type
    of *start*, *stop* and *step*.

.. function:: take(a, indices, out=None, queue=None)

    Return the :class:`Array` ``[a[indices[0]], ..., a[indices[n]]]``.
    For the moment, *a* must be a type that can be bound to a texture.

Conditionals
^^^^^^^^^^^^

.. function:: if_positive(criterion, then_, else_, out=None, queue=None)

    Return an array like *then_*, which, for the element at index *i*,
    contains *then_[i]* if *criterion[i]>0*, else *else_[i]*. (added in 0.94)

.. function:: maximum(a, b, out=None, queue=None)

    Return the elementwise maximum of *a* and *b*. (added in 0.94)

.. function:: minimum(a, b, out=None, queue=None)

    Return the elementwise minimum of *a* and *b*. (added in 0.94)

.. _reductions:

Reductions
^^^^^^^^^^

.. function:: sum(a, dtype=None, stream=None)

    .. versionadded: 2011.1

.. function:: dot(a, b, dtype=None, stream=None)

    .. versionadded: 2011.1

.. function:: subset_dot(subset, a, b, dtype=None, stream=None)

    .. versionadded: 2011.1

.. function:: max(a, stream=None)

    .. versionadded: 2011.1

.. function:: min(a, stream=None)

    .. versionadded: 2011.1

.. function:: subset_max(subset, a, stream=None)

    .. versionadded: 2011.1

.. function:: subset_min(subset, a, stream=None)

    .. versionadded: 2011.1

Elementwise Functions on :class:`Arrray` Instances
--------------------------------------------------

.. module:: pyopencl.clmath

The :mod:`pyopencl.clmath` module contains exposes array versions of the C
functions available in the OpenCL standard. (See table 6.8 in the spec.)

.. function:: acos(array, queue=None)
.. function:: acosh(array, queue=None)
.. function:: acospi(array, queue=None)

.. function:: asin(array, queue=None)
.. function:: asinh(array, queue=None)
.. function:: asinpi(array, queue=None)

.. function:: atan(array, queue=None)
.. TODO: atan2
.. function:: atanh(array, queue=None)
.. function:: atanpi(array, queue=None)
.. TODO: atan2pi

.. function:: cbrt(array, queue=None)
.. function:: ceil(array, queue=None)
.. TODO: copysign

.. function:: cos(array, queue=None)
.. function:: cosh(array, queue=None)
.. function:: cospi(array, queue=None)

.. function:: erfc(array, queue=None)
.. function:: erf(array, queue=None)
.. function:: exp(array, queue=None)
.. function:: exp2(array, queue=None)
.. function:: exp10(array, queue=None)
.. function:: expm1(array, queue=None)

.. function:: fabs(array, queue=None)
.. TODO: fdim
.. function:: floor(array, queue=None)
.. TODO: fma
.. TODO: fmax
.. TODO: fmin

.. function:: fmod(arg, mod, queue=None)

    Return the floating point remainder of the division `arg/mod`,
    for each element in `arg` and `mod`.

.. TODO: fract


.. function:: frexp(arg, queue=None)

    Return a tuple `(significands, exponents)` such that
    `arg == significand * 2**exponent`.

.. TODO: hypot

.. function:: ilogb(array, queue=None)
.. function:: ldexp(significand, exponent, queue=None)

    Return a new array of floating point values composed from the
    entries of `significand` and `exponent`, paired together as
    `result = significand * 2**exponent`.


.. function:: lgamma(array, queue=None)
.. TODO: lgamma_r

.. function:: log(array, queue=None)
.. function:: log2(array, queue=None)
.. function:: log10(array, queue=None)
.. function:: log1p(array, queue=None)
.. function:: logb(array, queue=None)

.. TODO: mad
.. TODO: maxmag
.. TODO: minmag


.. function:: modf(arg, queue=None)

    Return a tuple `(fracpart, intpart)` of arrays containing the
    integer and fractional parts of `arg`.

.. function:: nan(array, queue=None)

.. TODO: nextafter
.. TODO: remainder
.. TODO: remquo

.. function:: rint(array, queue=None)
.. TODO: rootn
.. function:: round(array, queue=None)

.. function:: sin(array, queue=None)
.. TODO: sincos
.. function:: sinh(array, queue=None)
.. function:: sinpi(array, queue=None)

.. function:: sqrt(array, queue=None)

.. function:: tan(array, queue=None)
.. function:: tanh(array, queue=None)
.. function:: tanpi(array, queue=None)
.. function:: tgamma(array, queue=None)
.. function:: trunc(array, queue=None)


Generating Arrays of Random Numbers
-----------------------------------

.. module:: pyopencl.clrandom

.. function:: rand(context, queue, shape, dtype)

    Return an array of `shape` filled with random values of `dtype`
    in the range [0,1).

Single-pass Custom Expression Evaluation
----------------------------------------

.. module:: pyopencl.elementwise

Evaluating involved expressions on :class:`pyopencl.array.Array` instances can be
somewhat inefficient, because a new temporary is created for each
intermediate result. The functionality in the module :mod:`pyopencl.elementwise`
contains tools to help generate kernels that evaluate multi-stage expressions
on one or several operands in a single pass.

.. class:: ElementwiseKernel(context, arguments, operation, name="kernel", preamble="", options=[])

    Generate a kernel that takes a number of scalar or vector *arguments*
    and performs the scalar *operation* on each entry of its arguments, if that
    argument is a vector.

    *arguments* is specified as a string formatted as a C argument list.
    *operation* is specified as a C assignment statement, without a semicolon.
    Vectors in *operation* should be indexed by the variable *i*.

    *name* specifies the name as which the kernel is compiled, 
    and *options* are passed unmodified to :meth:`pyopencl.Program.build`.

    *preamble* is a piece of C source code that gets inserted outside of the
    function context in the elementwise operation's kernel source code.

    .. method:: __call__(*args)

        Invoke the generated scalar kernel. The arguments may either be scalars or
        :class:`GPUArray` instances.

Here's a usage example::

    import pyopencl as cl
    import pyopencl.array as cl_array
    import numpy

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    n = 10
    a_gpu = cl_array.to_device(
            ctx, queue, numpy.random.randn(n).astype(numpy.float32))
    b_gpu = cl_array.to_device(
            ctx, queue, numpy.random.randn(n).astype(numpy.float32))

    from pyopencl.elementwise import ElementwiseKernel
    lin_comb = ElementwiseKernel(ctx,
            "float a, float *x, "
            "float b, float *y, "
            "float *z",
            "z[i] = a*x[i] + b*y[i]",
            "linear_combination")

    c_gpu = cl_array.empty_like(a_gpu)
    lin_comb(5, a_gpu, 6, b_gpu, c_gpu)

    import numpy.linalg as la
    assert la.norm((c_gpu - (5*a_gpu+6*b_gpu)).get()) < 1e-5

(You can find this example as :file:`examples/demo_elementwise.py` in the PyOpenCL
distribution.)

Custom Reductions
-----------------

.. module:: pycuda.reduction

.. class:: ReductionKernel(ctx, dtype_out, neutral, reduce_expr, map_expr=None, arguments=None, name="reduce_kernel", options="", preamble="")

    Generate a kernel that takes a number of scalar or vector *arguments*
    (at least one vector argument), performs the *map_expr* on each entry of
    the vector argument and then the *reduce_expr* on the outcome of that.
    *neutral* serves as an initial value. *preamble* offers the possibility
    to add preprocessor directives and other code (such as helper functions)
    to be added before the actual reduction kernel code.

    Vectors in *map_expr* should be indexed by the variable *i*. *reduce_expr*
    uses the formal values "a" and "b" to indicate two operands of a binary
    reduction operation. If you do not specify a *map_expr*, "in[i]" -- and
    therefore the presence of only one input argument -- is automatically
    assumed.

    *dtype_out* specifies the :class:`numpy.dtype` in which the reduction is
    performed and in which the result is returned. *neutral* is
    specified as float or integer formatted as string. *reduce_expr* and
    *map_expr* are specified as string formatted operations and *arguments*
    is specified as a string formatted as a C argument list. *name* specifies
    the name as which the kernel is compiled. *options* are passed
    unmodified to :meth:`pyopencl.Program.build`. *preamble* is specified
    as a string of code.

    .. method __call__(*args, queue=None)

    .. versionadded: 2011.1

Here's a usage example::

    a = pyopencl.array.arange(400, dtype=numpy.float32)
    b = pyopencl.array.arange(400, dtype=numpy.float32)

    krnl = ReductionKernel(ctx, numpy.float32, neutral="0",
            reduce_expr="a+b", map_expr="a[i]*b[i]",
            arguments="__global float *a, __global float *b")

    my_dot_prod = krnl(a, b).get()


Fast Fourier Transforms
-----------------------

Bogdan Opanchuk's `pyfft <http://pypi.python.org/pypi/pyfft>`_ package offers a
variety of GPU-based FFT implementations.

