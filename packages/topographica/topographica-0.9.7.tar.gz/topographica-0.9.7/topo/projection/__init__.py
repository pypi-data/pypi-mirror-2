"""
Projection classes.

A Projection is a connection between two Sheets, generally implemented
as a large set of ConnectionFields.

Any new Projection classes added to this directory will automatically
become available for any model.

$Id: __init__.py 8941 2008-08-21 13:40:59Z ceball $
"""
__version__='$Revision: 8941 $'

# Automatically discover all .py files in this directory, and import classes from basic.py. 
import os,fnmatch
from basic import *
__all__ = basic.__all__ + [f.split('.py')[0] for f in os.listdir(__path__[0]) if fnmatch.fnmatch(f,'[!._]*.py')]
del f,os,fnmatch
