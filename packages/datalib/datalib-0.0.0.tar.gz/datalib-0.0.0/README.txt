============
datalib
============

This is a package/library in python to work with time series data from xls file.
This is being developed under the project `AMBHAS <http://www.ambhas.com/>`_.


Installing datalib
======================

Installing datalib can be done by downloading source file (datalib--<version>.tar.gz),
and after unpacking issuing the command::

    python setup.py install

This requires the usual Distutils options available.

Or, download the datalib--<version>.tar.gz file and issue the command::
    
   pip /path/to/datalib--<version>.tar.gz

Or, directly using the pip::

   pip install datalib   


Usage
=========
Import required modules::

    import numpy as np
    from datalib import time_data

Read the time series data::

    data = time_data('/pata/to/file.xls')
    year = data.get('year')
    month = data.get('month')
    gw_observed = 839-data.get('gw')
  
Changelog
=========

0.0.0 (July 2011)
------------------
- Initial release


Any questions/comments
=========================
If you have any comment/suggestion/question, 
please feel free to write me at satkumartomer@gmail.com

So far, the documents are not well explained, 
I will be updating them soon.




