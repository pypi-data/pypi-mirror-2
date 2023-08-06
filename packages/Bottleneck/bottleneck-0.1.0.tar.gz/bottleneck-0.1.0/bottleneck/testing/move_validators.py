"""
Alternative methods (non-Cython) of calculating moving window statistics.

These function are slow but useful for unit testing.
"""

import numpy as np
from scipy.ndimage import convolve1d

__all__ = ['move_sum', 'move_func']


# SUM -----------------------------------------------------------------------

def move_sum(arr, window, axis=-1, method='filter'):
    """
    Moving window sum along the specified axis, ignoring NaNs.
    
    Parameters
    ----------
    arr : ndarray
        Input array.
    window : int
        The number of elements in the moving window.
    axis : int, optional
        The axis over which to perform the moving sum. By default the moving
        sum is taken over the last axis (-1).
    method : str, optional
        The following moving window methods are available:
            ==========  =====================================
            'filter'    scipy.ndimage.convolve1d (default)
            'strides'   strides tricks (ndim < 4)
            'loop'      brute force python loop
            ==========  =====================================

    Returns
    -------
    y : ndarray
        The moving sum of the input array along the specified axis, ignoring
        NaNs. (A window with all NaNs returns NaN for the window sum.) The
        output has the same shape as the input.
        
    Notes
    -----
    Care should be taken when using the `cumsum` moving window method. On
    some problem sizes it is fast; however, it is possible to get small
    negative values even if the input is non-negative.

    Examples
    --------
    >>> arr = np.array([1, 2, np.nan, 4])
    >>> la.farray.mov_nansum(arr, window=2, axis=0)
    array([ NaN,   3.,   2.,   4.])

    """
    arr = np.array(arr, copy=False)
    if method == 'filter':
        y = move_sum_filter(arr, window, axis=axis)
    elif method == 'strides':
        y = move_func_strides(np.nansum, arr, window, axis=axis)
    elif method == 'loop':
        y = move_func_loop(np.nansum, arr, window, axis=axis)
    else:
        msg = "`method` must be 'filter', 'strides', or 'loop'."
        raise ValueError, msg
    return y

def move_sum_filter(arr, window, axis=-1):
    """
    Moving sum (ignoring NaNs) along specified axis using the filter method.
    
    Parameters
    ----------
    arr : ndarray
        Input array.
    window : int
        The number of elements in the moving window.
    axis : int, optional
        The axis over which to perform the moving sum. By default the moving
        sum is taken over the last axis (-1).
    
    Returns
    -------
    y : ndarray
        The moving sum (ignoring NaNs) of the input array along the specified
        axis.(A window with all NaNs returns NaN for the window sum.) The
        output has the same shape as the input.

    Notes
    -----
    The calculation of the sums uses scipy.ndimage.convolve1d. 

    Examples
    --------
    >>> from la.farray.mov import mov_sum_filter
    >>> arr = np.array([1, 2, np.nan, 4, 5, 6, 7])
    >>> mov_nansum_filter(arr, window=2, axis=0)
    array([ NaN,   3.,   2.,   4.,   9.,  11.,  13.])

    """
    if axis == None:
        raise ValueError, "An `axis` value of None is not supported."
    if window < 1:  
        raise ValueError, "`window` must be at least 1."
    if window > arr.shape[axis]:
        raise ValueError, "`window` is too long."  
    arr = arr.astype(float)
    nrr = np.isnan(arr)
    arr[nrr] = 0
    nrr = nrr.astype(int)
    w = np.ones(window, dtype=int)
    x0 = (1 - window) // 2
    convolve1d(arr, w, axis=axis, mode='constant', cval=np.nan, origin=x0,
               output=arr)
    convolve1d(nrr, w, axis=axis, mode='constant', cval=0, origin=x0,
               output=nrr)
    arr[nrr == window] = np.nan
    return arr

# MEAN ----------------------------------------------------------------------

def mov_mean(arr, window, axis=-1, method='filter'):
    """
    Moving window mean along the specified axis.
    
    Parameters
    ----------
    arr : ndarray
        Input array.
    window : int
        The number of elements in the moving window.
    axis : int, optional
        The axis over which to perform the moving mean. By default the moving
        mean is taken over the last axis (-1).
    method : str, optional
        The following moving window methods are available:
            ==========  =====================================
            'filter'    scipy.ndimage.convolve1d (default)
            'strides'   strides tricks (ndim < 4)
            'loop'      brute force python loop
            ==========  =====================================

    Returns
    -------
    y : ndarray
        The moving mean of the input array along the specified axis. The output
        has the same shape as the input.

    Examples
    --------
    >>> arr = np.array([1, 2, 3, 4])
    >>> la.farray.mov_mean(arr, window=2, axis=0)
    array([ NaN,  1.5,  2.5,  3.5])
    
    """
    if method == 'filter':
        y = mov_mean_filter(arr, window, axis=axis)
    elif method == 'strides':
        y = mov_func_strides(np.mean, arr, window, axis=axis)
    elif method == 'loop':
        y = mov_func_loop(np.mean, arr, window, axis=axis)
    else:
        msg = "`method` must be 'filter', 'strides', or 'loop'."
        raise ValueError, msg
    return y

def mov_nanmean(arr, window, axis=-1, method='filter'):
    """
    Moving window mean along the specified axis, ignoring NaNs.
    
    Parameters
    ----------
    arr : ndarray
        Input array.
    window : int
        The number of elements in the moving window.
    axis : int, optional
        The axis over which to perform the moving mean. By default the moving
        mean is taken over the last axis (-1).
    method : str, optional
        The following moving window methods are available:
            ==========  =====================================
            'filter'    scipy.ndimage.convolve1d (default)
            'strides'   strides tricks (ndim < 4)
            'loop'      brute force python loop
            ==========  =====================================

    Returns
    -------
    y : ndarray
        The moving mean of the input array along the specified axis, ignoring
        NaNs. (A window with all NaNs returns NaN for the window mean.) The
        output has the same shape as the input.
    
    Notes
    -----
    Care should be taken when using the `cumsum` moving window method. On
    some problem sizes it is fast; however, it is possible to get small
    negative values even if the input is non-negative.

    Examples
    --------
    >>> arr = np.array([1, 2, np.nan, 4])
    >>> la.farray.mov_nanmean(arr, window=2, axis=0)
    array([ NaN,  1.5,  2. ,  4. ])
    
    """
    if method == 'filter':
        y = mov_nanmean_filter(arr, window, axis=axis)
    elif method == 'strides':
        y = mov_func_strides(nanmean, arr, window, axis=axis)
    elif method == 'loop':
        y = mov_func_loop(nanmean, arr, window, axis=axis)
    else:
        msg = "`method` must be 'filter', 'cumsum', 'strides', or 'loop'."
        raise ValueError, msg
    return y

def mov_mean_filter(arr, window, axis=-1):
    "Moving window mean implemented with a filter."
    if axis == None:
        raise ValueError, "An `axis` value of None is not supported."
    if window < 1: 
        raise ValueError, "`window` must be at least 1."
    if window > arr.shape[axis]:
        raise ValueError, "`window` is too long."  
    arr = arr.astype(float)
    w = np.empty(window)
    w.fill(1.0 / window)
    x0 = (1 - window) // 2
    convolve1d(arr, w, axis=axis, mode='constant', cval=np.nan, origin=x0,
               output=arr)
    return arr

def mov_nanmean_filter(arr, window, axis=-1):
    "Moving window nanmean implemented with a filter."
    if axis == None:
        raise ValueError, "An `axis` value of None is not supported."
    if window < 1:  
        raise ValueError, "`window` must be at least 1."
    if window > arr.shape[axis]:
        raise ValueError, "`window` is too long."  
    arr = arr.astype(float)
    nrr = np.isnan(arr)
    arr[nrr] = 0
    nrr = nrr.astype(int)
    w = np.ones(window, dtype=int)
    x0 = (1 - window) // 2
    convolve1d(arr, w, axis=axis, mode='constant', cval=np.nan, origin=x0,
               output=arr)
    convolve1d(nrr, w, axis=axis, mode='constant', cval=0, origin=x0,
               output=nrr)
    arr /= (window - nrr)
    arr[nrr == window] = np.nan
    return arr

# GENERAL --------------------------------------------------------------------

def move_func(func, arr, window, axis=-1, method='loop', **kwargs):
    """
    Generic moving window function along the specified axis.
    
    Parameters
    ----------
    func : function
        A reducing function such as np.sum, np.max, or np.median that takes
        a Numpy array and axis and, optionally, key word arguments as input.
    arr : ndarray
        Input array.
    window : int
        The number of elements in the moving window.
    axis : int, optional
        The axis over which to evaluate `func`. By default the window moves
        along the last axis (-1).
    method : str, optional
        The following moving window methods are available:
            ==========  =====================================
            'loop'      brute force python loop (default)
            'strides'   strides tricks (ndim < 4)
            ==========  =====================================

    Returns
    -------
    y : ndarray
        A moving window evaluation of `func` along the specified axis of the
        input array. The output has the same shape as the input.

    Examples
    --------
    >>> arr = np.arange(4)
    >>> la.farray.mov_func(np.sum, arr, window=2)
    array([ NaN,   1.,   3.,   5.])

    which give the same result as:

    >>> la.farray.mov_sum(arr, window=2)
    array([ NaN,   1.,   3.,   5.])

    """
    if method == 'strides':
        y = move_func_strides(func, arr, window, axis=axis, **kwargs)
    elif method == 'loop':
        y = move_func_loop(func, arr, window, axis=axis)
    else:
        msg = "`method` must be 'strides' or 'loop'."
        raise ValueError, msg
    return y

def move_func_loop(func, arr, window, axis=-1, **kwargs):
    "Generic moving window function implemented with a python loop."
    if axis == None:
        raise ValueError, "An `axis` value of None is not supported."
    if window < 1:  
        raise ValueError, "`window` must be at least 1."
    if window > arr.shape[axis]:
        raise ValueError, "`window` is too long."
    y = np.empty(arr.shape)
    y.fill(np.nan)
    idx1 = [slice(None)] * arr.ndim
    idx2 = list(idx1)
    for i in range(window - 1, arr.shape[axis]):
        idx1[axis] = slice(i + 1 - window, i + 1)
        idx2[axis] = i
        y[idx2] = func(arr[idx1], axis=axis, **kwargs)
    return y    

def move_func_strides(func, arr, window, axis=-1, **kwargs):
    "Generic moving window function implemented with strides."
    if axis == None:
        raise ValueError, "An `axis` value of None is not supported."
    if window < 1:  
        raise ValueError, "`window` must be at least 1."
    if window > arr.shape[axis]:
        raise ValueError, "`window` is too long."
    ndim = arr.ndim
    as_strided = np.lib.stride_tricks.as_strided
    idx = range(ndim)
    axis = idx[axis]
    arrshape0 = tuple(arr.shape)
    if axis >= ndim:
        raise IndexError, "`axis` is out of range."
    if ndim == 1:
        strides = arr.strides
        shape = (arr.size - window + 1, window)
        strides = 2 * strides
        z = as_strided(arr, shape=shape, strides=strides)
        y = func(z, axis=1, **kwargs)
    elif ndim == 2:
        if axis == 1:
            arr = arr.T
        strides = arr.strides
        shape = (arr.shape[0] - window + 1, window, arr.shape[1]) 
        strides = (strides[0],) + strides 
        z = as_strided(arr, shape=shape, strides=strides)
        y = func(z, axis=1, **kwargs)
        if axis == 1:
            y = y.T    
    elif ndim == 3:
        if axis > 0:
            arr = arr.swapaxes(0, axis)
        strides = arr.strides
        shape = (arr.shape[0]-window+1, window, arr.shape[1], arr.shape[2])
        strides = (strides[0],) + strides
        z = as_strided(arr, shape=shape, strides=strides)
        y = func(z, axis=1, **kwargs)
        if axis > 0:
            y = y.swapaxes(0, axis)
    else:
        raise ValueError, "Only 1d, 2d, and 3d input arrays are supported."
    ynan = np.empty(arrshape0)
    ynan.fill(np.nan)
    index = [slice(None)] * ndim 
    index[axis] = slice(window - 1, None)
    ynan[index] = y
    return ynan
