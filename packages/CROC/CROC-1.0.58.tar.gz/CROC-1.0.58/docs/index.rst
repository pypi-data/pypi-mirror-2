================
The CROC Package
================
A package for calculating ROC curves and Concentrated ROC (CROC) curves.

This pure-python package is designed to be a standardized implementation of performance curves
and metrics for use either in python scripts or through a simple commandline interface. As a standardized implementation
its output is robust enough to be using in publishable scientific work.

With this package, one can easily:

#. Compute the coordinates of both Accumulation Curves and ROC curves.
#. Handle ties appropriately using several methods.
#. Compute the BEDROC metric.
#. Vertically add and average the performance curves of several cross-validation folds.
#. Focus on the early part of the ROC curve by using several soon to be published x-axis transforms.


The docstrings in this module are fairly complete and the scripts provide simple access to
the most common functions. Further documentation can be found here:

.. toctree::
    :maxdepth: 2

    install
    scripts
    formats
    r
    api

Development Status
-------------------

On 3/14/2010 this project has officially moved out of beta and is designated a stable release.
Please email the `author <http://swami.wustl.edu/>`_ if you discover any bugs. 

