"""
Objects capable of generating a two-dimensional array of values.

Such patterns can be used as input to a Sheet, as initial or fixed
weight patterns, or for any other purpose where a two-dimensional
pattern may be needed.  Any new PatternGenerator classes added to this
directory will automatically become available for any model.

$Id: __init__.py 8943 2008-08-21 13:47:25Z ceball $
"""
__version__='$Revision: 8943 $'

# Automatically discover all .py files in this directory, and import classes from basic.py. 
import os,fnmatch
from basic import *
__all__ = basic.__all__ + [f.split('.py')[0] for f in os.listdir(__path__[0]) if fnmatch.fnmatch(f,'[!._]*.py')]
del f,os,fnmatch

# CB: temporarily hide the audio module until it works and is properly
# supported by the GUI etc.
__all__.remove('audio')
