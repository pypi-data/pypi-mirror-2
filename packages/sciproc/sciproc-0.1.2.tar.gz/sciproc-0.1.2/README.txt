===========
sciproc
===========


Sciproc in development provides tools to select, edit, convert scientific
(observed, model-generated) data. It needs Numpy.
Currently selection from 1D data by coordinates or certain timestep is
implemented. However selecting, interpolating and editing procedures for
multidimensional data is planned in the near future.  You might want to use
it if you have have any observational data and you want to select a period,
make a selection with a certain timestep or make an interpolation. The aim
is to make a full python replacement which provide all operations from the
cdo (an ncdf package). It should be working with normal numpy data. However,
if you want to process netcdf-files, we recomend to use the ncdf-extra
interface which directly uses this library and which also provides
command-line tools to process netcdf-files directly. Typical usage often
looks like this::

    #!/usr/bin/env python

    from numpy import *
    from sciproc import *

    # select data from a 1-D array:
    data = array([1.0,2.0,4.0,2.5])
    incoords = array([0.0,1.0,2.0,3.0])
    print(scisel(data,coords = incoords,outcoords = array([1.0,2.0]))


A Section
=========


A Sub-Section
-------------


