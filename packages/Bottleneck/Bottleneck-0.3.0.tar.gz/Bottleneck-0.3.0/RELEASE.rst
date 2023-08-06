
=============
Release Notes
=============

These are the major changes made in each release. For details of the changes
see the commit log at http://github.com/kwgoodman/bottleneck

Bottleneck 0.3.0
================

*Release date: 2010-01-19*

The third release of Bottleneck is twice as fast for small input arrays and
contains 10 new functions.

**Faster**

- All functions are faster (less overhead in selector functions) 

**New functions**

- nansum()
- move_sum()
- move_nansum()  
- move_mean()  
- move_std()
- move_nanstd()  
- move_min()
- move_nanmin()
- move_max()
- move_nanmax()

**Enhancements**

- You can now specify the dtype and axis to use in the benchmark timings
- Improved documentation and more unit tests  

**Breaks from 0.2.0**

- Moving window functions now default to axis=-1 instead of axis=0
- Low-level moving window selector functions no longer take window as input 

**Bug fix**

- int input array resulted in call to slow, non-cython version of move_nanmean 

Older versions
==============

Release notes from past releases.

Bottleneck 0.2.0
----------------

*Release date: 2010-12-27*

The second release of Bottleneck is faster, contains more functions, and
supports more dtypes.

**Faster**

- All functions faster (less overhead) when output is not a scalar
- Faster nanmean() for 2d, 3d arrays containing NaNs when axis is not None

**New functions**

- nanargmin()
- nanargmax()
- nanmedian()

**Enhancements**

- Added support for float32
- Fallback to slower, non-Cython functions for unaccelerated ndim/dtype  
- Scipy is no longer a dependency
- Added support for older versions of NumPy (1.4.1)
- All functions are now templated for dtype and axis  
- Added a sandbox for prototyping of new Bottleneck functions
- Rewrote benchmarking code  
- Embed function signatures in docstrings

**Breaks from 0.1.0**

- To run benchmark use bn.bench() instead of bn.benchit()

Bottleneck 0.1.0
----------------

*Release date: 2010-12-01*

Preview release of Bottleneck.
