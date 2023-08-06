==================
Function reference
==================

Bottleneck provides the following functions:

======================= =======================================================================================================================
NumPy/SciPy             :meth:`median <bottleneck.median>`, :meth:`nanmedian <bottleneck.nanmedian>`, :meth:`nansum <bottleneck.nansum>`,
                        :meth:`nanmin <bottleneck.nanmin>`, :meth:`nanmax <bottleneck.nanmax>`, :meth:`nanmean <bottleneck.nanmean>`,
                        :meth:`nanstd <bottleneck.nanstd>`, :meth:`nanargmin <bottleneck.nanargmin>`, :meth:`nanargmax <bottleneck.nanargmax>` 
Functions               :meth:`nanvar <bottleneck.nanvar>` 
Moving window           :meth:`move_sum <bottleneck.move_sum>`, :meth:`move_nansum <bottleneck.move_nansum>`,
                        :meth:`move_mean <bottleneck.move_mean>`, :meth:`move_nanmean <bottleneck.move_nanmean>`,
                        :meth:`move_std <bottleneck.move_std>`, :meth:`move_nanstd <bottleneck.move_nanstd>`,
                        :meth:`move_min <bottleneck.move_min>`, :meth:`move_nanmin <bottleneck.move_nanmin>`,
                        :meth:`move_max <bottleneck.move_max>`, :meth:`move_nanmax <bottleneck.move_nanmax>`
Group by                :meth:`group_nanmean <bottleneck.group_nanmean>`
======================= =======================================================================================================================


NumPy/SciPy
-----------

Fast replacements for NumPy and SciPy functions.

------------

.. autofunction:: bottleneck.median

------------
             
.. autofunction:: bottleneck.nanmedian

------------

.. autofunction:: bottleneck.nansum

------------

.. autofunction:: bottleneck.nanmin

------------

.. autofunction:: bottleneck.nanmax

------------
             
.. autofunction:: bottleneck.nanmean

------------

.. autofunction:: bottleneck.nanstd

------------

.. autofunction:: bottleneck.nanargmin

------------

.. autofunction:: bottleneck.nanargmax


Functions
---------

Miscellaneous functions.

------------

.. autofunction:: bottleneck.nanvar


Moving window functions
-----------------------

Moving window functions with a 1d window.

------------

.. autofunction:: bottleneck.move_sum

------------

.. autofunction:: bottleneck.move_nansum

------------

.. autofunction:: bottleneck.move_mean

------------

.. autofunction:: bottleneck.move_nanmean

------------

.. autofunction:: bottleneck.move_std

------------

.. autofunction:: bottleneck.move_nanstd

------------

.. autofunction:: bottleneck.move_min

------------

.. autofunction:: bottleneck.move_nanmin

------------

.. autofunction:: bottleneck.move_max

------------

.. autofunction:: bottleneck.move_nanmax


Group functions
---------------

Calculations done on like-labeled elements.

------------

.. autofunction:: bottleneck.group_nanmean
