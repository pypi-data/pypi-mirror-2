"""
Analysis tools for Topographica, other than plotting tools.

$Id: __init__.py 9520 2008-10-24 21:49:12Z jbednar $
"""

__version__='$Revision: 9520 $'

# Automatically discover all .py files in this directory, and import functions from basic.py. 
import os,fnmatch
__all__ = [f.split('.py')[0] for f in os.listdir(__path__[0]) if fnmatch.fnmatch(f,'[!._]*.py')]
del f,os,fnmatch

