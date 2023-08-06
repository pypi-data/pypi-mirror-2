
cdef np.int32_t MININT32 = np.iinfo(np.int32).min
cdef np.int64_t MININT64 = np.iinfo(np.int64).min

cdef dict max_dict = {}

#          Dim dtype axis
max_dict[(1, f64, 0)] = max_1d_float64_axis0
max_dict[(1, f64, N)] = max_1d_float64_axis0
max_dict[(2, f64, 0)] = max_2d_float64_axis0
max_dict[(2, f64, 1)] = max_2d_float64_axis1
max_dict[(2, f64, N)] = max_2d_float64_axisNone
max_dict[(3, f64, 0)] = max_3d_float64_axis0
max_dict[(3, f64, 1)] = max_3d_float64_axis1
max_dict[(3, f64, 2)] = max_3d_float64_axis2
max_dict[(3, f64, N)] = max_3d_float64_axisNone

max_dict[(1, i32, 0)] = max_1d_int32_axis0
max_dict[(1, i32, N)] = max_1d_int32_axis0
max_dict[(2, i32, 0)] = max_2d_int32_axis0
max_dict[(2, i32, 1)] = max_2d_int32_axis1
max_dict[(2, i32, N)] = max_2d_int32_axisNone
max_dict[(3, i32, 0)] = max_3d_int32_axis0
max_dict[(3, i32, 1)] = max_3d_int32_axis1
max_dict[(3, i32, 2)] = max_3d_int32_axis2
max_dict[(3, i32, N)] = max_3d_int32_axisNone

max_dict[(1, i64, 0)] = max_1d_int64_axis0
max_dict[(1, i64, N)] = max_1d_int64_axis0
max_dict[(2, i64, 0)] = max_2d_int64_axis0
max_dict[(2, i64, 1)] = max_2d_int64_axis1
max_dict[(2, i64, N)] = max_2d_int64_axisNone
max_dict[(3, i64, 0)] = max_3d_int64_axis0
max_dict[(3, i64, 1)] = max_3d_int64_axis1
max_dict[(3, i64, 2)] = max_3d_int64_axis2
max_dict[(3, i64, N)] = max_3d_int64_axisNone


def max(arr, axis=None):
    """
    Maximum along the specified axis, ignoring NaNs.

    Parameters
    ----------
    arr : array_like
        Input array. If `arr` is not an array, a conversion is attempted.
    axis : {int, None}, optional
        Axis along which the maximum is computed. The default is to compute
        the maximum of the flattened array.

    Returns
    -------
    y : ndarray
        An array with the same shape as `arr`, with the specified axis removed.
        If `arr` is a 0-d array, or if axis is None, a scalar is returned.
    
    Examples
    --------
    >>> bn.max(1)
    1
    >>> bn.max([1])
    1
    >>> bn.max([1, np.nan])
    1.0
    >>> a = np.array([[1, 4], [1, np.nan]])
    >>> bn.max(a)
    4.0
    >>> bn.max(a, axis=0)
    array([ 1.,  4.])
    
    """
    func, arr = max_selector(arr, axis)
    return func(arr)

def max_selector(arr, axis):
    """
    Return maximum function and array that matches `arr` and `axis`.
    
    Under the hood Bottleneck uses a separate Cython function for each
    combination of ndim, dtype, and axis. A lot of the overhead in bn.max()
    is in checking that `axis` is within range, converting `arr` into an
    array (if it is not already an array), and selecting the function to use
    to calculate the maximum.

    You can get rid of the overhead by doing all this before you, for example,
    enter an inner loop, by using the this function.

    Parameters
    ----------
    arr : array_like
        Input array. If `arr` is not an array, a conversion is attempted.
    axis : {int, None}, optional
        Axis along which the maximum is to be computed. The default
        (axis=None) is to compute the maximum of the flattened array.
    
    Returns
    -------
    func : function
        The maximum function that matches the number of dimensions and
        dtype of the input array and the axis along which you wish to find
        the maximum.
    a : ndarray
        If the input array `arr` is not a ndarray, then `a` will contain the
        result of converting `arr` into a ndarray.

    Examples
    --------
    Create a numpy array:

    >>> arr = np.array([1.0, 2.0, 3.0])
    
    Obtain the function needed to determine the maximum of `arr` along
    axis=0:

    >>> func, a = bn.func.max_selector(arr, axis=0)
    >>> func
    <built-in function max_1d_float64_axis0> 
    
    Use the returned function and array to determaxe the maximum:
    
    >>> func(a)
    3.0

    """
    cdef np.ndarray a = np.array(arr, copy=False)
    cdef int ndim = a.ndim
    cdef np.dtype dtype = a.dtype
    cdef int size = a.size
    if size == 0:
        msg = "numpy.nanmax() raises on size=0 input; so Bottleneck does too." 
        raise ValueError, msg
    if axis != None:
        if axis < 0:
            axis += ndim
        if (axis < 0) or (axis >= ndim):
            raise ValueError, "axis(=%d) out of bounds" % axis
    cdef tuple key = (ndim, dtype, axis)
    try:
        func = max_dict[key]
    except KeyError:
        tup = (str(ndim), str(dtype))
        raise TypeError, "Unsupported ndim/dtype (%s/%s)." % tup
    return func, a

# One dimensional -----------------------------------------------------------

@cython.boundscheck(False)
@cython.wraparound(False)
def max_1d_int32_axis0(np.ndarray[np.int32_t, ndim=1] a):
    "max of 1d numpy array with dtype=np.int32 along axis=0."
    cdef Py_ssize_t i
    cdef int n0 = a.shape[0]
    cdef np.int32_t amax = MININT32, ai
    for i in range(n0):
        ai = a[i]
        if ai >= amax:
            amax = ai
    return np.int32(amax)

@cython.boundscheck(False)
@cython.wraparound(False)
def max_1d_int64_axis0(np.ndarray[np.int64_t, ndim=1] a):
    "max of 1d numpy array with dtype=np.int64 along axis=0."
    cdef Py_ssize_t i
    cdef int n0 = a.shape[0]
    cdef np.int64_t amax = MININT64, ai
    for i in range(n0):
        ai = a[i]
        if ai >= amax:
            amax = ai
    return np.int64(amax)

@cython.boundscheck(False)
@cython.wraparound(False)
def max_1d_float64_axis0(np.ndarray[np.float64_t, ndim=1] a):
    "max of 1d numpy array with dtype=np.float64 along axis=0."
    cdef Py_ssize_t i
    cdef int n0 = a.shape[0], allnan = 1
    cdef np.float64_t amax = np.NINF, ai
    for i in range(n0):
        ai = a[i]
        if ai >= amax:
            amax = ai
            allnan = 0
    if allnan == 0:
        return np.float64(amax)
    else:
        return NAN

# Two dimensional -----------------------------------------------------------

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_int32_axis0(np.ndarray[np.int32_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.int32 along axis=0."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1]
    cdef np.int32_t amax, ai  
    cdef np.ndarray[np.int32_t, ndim=1] y = np.empty(n1, dtype=np.int32)
    for j in range(n1):
        amax = MININT32
        for i in range(n0):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
        y[j] = amax    
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_int32_axis1(np.ndarray[np.int32_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.int32 along axis=1"
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1]
    cdef np.int32_t amax 
    cdef np.ndarray[np.int32_t, ndim=1] y = np.empty(n0, dtype=np.int32)
    for i in range(n0):
        amax = MININT32
        for j in range(n1):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
        y[i] = amax    
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_int32_axisNone(np.ndarray[np.int32_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.int32 along axis=None."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1]
    cdef np.int32_t amax = MININT32, ai
    for i in range(n0):
        for j in range(n1):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
    return np.int32(amax) 

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_int64_axis0(np.ndarray[np.int64_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.int64 along axis=0."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1]
    cdef np.int64_t amax, ai  
    cdef np.ndarray[np.int64_t, ndim=1] y = np.empty(n1, dtype=np.int64)
    for j in range(n1):
        amax = MININT64
        for i in range(n0):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
        y[j] = amax    
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_int64_axis1(np.ndarray[np.int64_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.int64 along axis=1"
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1]
    cdef np.int64_t amax, ai 
    cdef np.ndarray[np.int64_t, ndim=1] y = np.empty(n0, dtype=np.int64)
    for i in range(n0):
        amax = MININT64
        for j in range(n1):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
        y[i] = amax    
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_int64_axisNone(np.ndarray[np.int64_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.int64 along axis=None."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1]
    cdef np.int64_t amax = MININT64, ai
    for i in range(n0):
        for j in range(n1):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
    return np.int64(amax) 

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_float64_axis0(np.ndarray[np.float64_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.float64 along axis=0."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1], allnan 
    cdef np.float64_t amax, ai 
    cdef np.ndarray[np.float64_t, ndim=1] y = np.empty(n1, dtype=np.float64)
    for j in range(n1):
        amax = np.NINF
        allnan = 1
        for i in range(n0):
            ai = a[i,j]
            if ai >= amax :
                amax = ai
                allnan = 0
        if allnan == 0:       
            y[j] = amax
        else:
            y[j] = NAN
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_float64_axis1(np.ndarray[np.float64_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.float64 along axis=1."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1], allnan
    cdef np.float64_t amax, ai  
    cdef np.ndarray[np.float64_t, ndim=1] y = np.empty(n0, dtype=np.float64)
    for j in range(n0):
        amax = np.NINF
        allnan = 1
        for i in range(n1):
            ai = a[j,i]
            if ai >= amax:
                amax = ai
                allnan = 0
        if allnan == 0:       
            y[j] = amax
        else:
            y[j] = NAN
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_2d_float64_axisNone(np.ndarray[np.float64_t, ndim=2] a):
    "max of 2d numpy array with dtype=np.float64 along axis=None."
    cdef Py_ssize_t i, j
    cdef int n0 = a.shape[0], n1 = a.shape[1], allnan = 1
    cdef np.float64_t amax = np.NINF, ai
    for i in range(n0):
        for j in range(n1):
            ai = a[i,j]
            if ai >= amax:
                amax = ai
                allnan = 0
    if allnan == 0:
        return np.float64(amax)
    else:
        return NAN

# Three dimensional ---------------------------------------------------------

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int32_axis0(np.ndarray[np.int32_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int32 along axis=0."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int32_t amax, ai  
    cdef np.ndarray[np.int32_t, ndim=2] y = np.empty((n1, n2), dtype=np.int32)
    for j in range(n1):
        for k in range(n2):
            amax = MININT32
            for i in range(n0):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
            y[j, k] = amax    
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int32_axis1(np.ndarray[np.int32_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int32 along axis=1"
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax, ai   
    cdef np.ndarray[np.int32_t, ndim=2] y = np.empty((n0, n2), dtype=np.int32)
    for i in range(n0):
        for k in range(n2):
            amax = MININT32
            for j in range(n1):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
            y[i, k] = amax 
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int32_axis2(np.ndarray[np.int32_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int32 along axis=2"
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax, ai   
    cdef np.ndarray[np.int32_t, ndim=2] y = np.empty((n0, n1), dtype=np.int32)
    for i in range(n0):
        for j in range(n1):
            amax = MININT32
            for k in range(n2):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
            y[i, j] = amax 
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int32_axisNone(np.ndarray[np.int32_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int32 along axis=None."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax = MININT64, ai
    for i in range(n0):
        for j in range(n1):
            for k in range(n2):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
    return np.int32(amax) 

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int64_axis0(np.ndarray[np.int64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int64 along axis=0."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax, ai  
    cdef np.ndarray[np.int64_t, ndim=2] y = np.empty((n1, n2), dtype=np.int64)
    for j in range(n1):
        for k in range(n2):
            amax = MININT64
            for i in range(n0):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
            y[j, k] = amax    
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int64_axis1(np.ndarray[np.int64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int64 along axis=1"
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax, ai 
    cdef np.ndarray[np.int64_t, ndim=2] y = np.empty((n0, n2), dtype=np.int64)
    for i in range(n0):
        for k in range(n2):
            amax = MININT64
            for j in range(n1):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
            y[i, k] = amax 
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int64_axis2(np.ndarray[np.int64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int64 along axis=2"
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax, ai 
    cdef np.ndarray[np.int64_t, ndim=2] y = np.empty((n0, n1), dtype=np.int64)
    for i in range(n0):
        for j in range(n1):
            amax = MININT64
            for k in range(n2):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
            y[i, j] = amax 
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_int64_axisNone(np.ndarray[np.int64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.int64 along axis=None."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2]
    cdef np.int64_t amax = MININT64, ai
    for i in range(n0):
        for j in range(n1):
            for k in range(n2):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
    return np.int64(amax) 

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_float64_axis0(np.ndarray[np.float64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.float64 along axis=0."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2], allnan
    cdef np.float64_t amax, ai
    cdef np.ndarray[np.float64_t, ndim=2] y = np.empty((n1, n2),
                                                       dtype=np.float64)
    for j in range(n1):
        for k in range(n2):
            amax = np.NINF
            allnan = 1
            for i in range(n0):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
                    allnan = 0
            if allnan == 0:   
                y[j, k] = amax
            else:
                y[j, k] = NAN
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_float64_axis1(np.ndarray[np.float64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.float64 along axis=1."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2], allnan
    cdef np.float64_t amax, ai
    cdef np.ndarray[np.float64_t, ndim=2] y = np.empty((n0, n2),
                                                       dtype=np.float64)
    for i in range(n0):
        for k in range(n2):
            amax = np.NINF
            allnan = 1
            for j in range(n1):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
                    allnan = 0
            if allnan == 0:   
                y[i, k] = amax
            else:
                y[i, k] = NAN
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_float64_axis2(np.ndarray[np.float64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.float64 along axis=2."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2], allnan
    cdef np.float64_t amax, ai
    cdef np.ndarray[np.float64_t, ndim=2] y = np.empty((n0, n1),
                                                       dtype=np.float64)
    for i in range(n0):
        for j in range(n1):
            amax = np.NINF
            allnan = 1
            for k in range(n2):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
                    allnan = 0
            if allnan == 0:   
                y[i, j] = amax
            else:
                y[i, j] = NAN
    return y

@cython.boundscheck(False)
@cython.wraparound(False)
def max_3d_float64_axisNone(np.ndarray[np.float64_t, ndim=3] a):
    "max of 3d numpy array with dtype=np.float64 along axis=None."
    cdef Py_ssize_t i, j, k
    cdef int n0 = a.shape[0], n1 = a.shape[1], n2 = a.shape[2], allnan = 1
    cdef np.float64_t amax = np.NINF, ai
    for i in range(n0):
        for j in range(n1):
            for k in range(n2):
                ai = a[i,j,k]
                if ai >= amax:
                    amax = ai
                    allnan = 0
    if allnan == 0:                
        return np.float64(amax)
    else:
        return NAN
