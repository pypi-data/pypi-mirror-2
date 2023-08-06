==============================
stats -- calculator statistics
==============================

Introduction
------------

stats provides common statistics functions including:

- mean, median, mode
- geometric, harmonic and quadratic means
- variance and standard deviation (both for samples and populations)
- covariance and Pearson's correlation coefficient
- linear regression fitting
- plus others.


Requires Python 2.5, 2.6 or 2.7.


Installation
------------

stats requires Python 2.5, 2.6 or 2.7. To install, do the usual:

    python setup.py install


Licence
-------

stats is licenced under the MIT Licence. See the LICENCE.txt file
and the header of stats.py.


Self-test
---------

You can run the module's doctests by executing the file from the commandline.
On most Linux or UNIX systems:

    $ chmod u+x stats.py  # this is only needed once
    $ ./stats.py

or:

    $ python stats.py

If all the doctests pass, no output will be printed. To get verbose output,
run with the -v switch:

    $ python stats.py -v


Known Issues
------------

See the CHANGES.txt file for a list of known issues.

