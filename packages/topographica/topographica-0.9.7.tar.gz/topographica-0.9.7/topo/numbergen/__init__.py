"""
Callable objects that generate numbers according to different distributions.

$Id: __init__.py 9019 2008-08-27 13:37:29Z jbednar $
"""
__version__='$Revision: 8943 $'

# Automatically discover all .py files in this directory, and import classes from basic.py. 
import os,fnmatch
from basic import *
__all__ = basic.__all__ + [f.split('.py')[0] for f in os.listdir(__path__[0]) if fnmatch.fnmatch(f,'[!._]*.py')]
del f,os,fnmatch
