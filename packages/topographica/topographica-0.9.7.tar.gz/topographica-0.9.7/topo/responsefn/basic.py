"""
Basic response functions.

$Id: basic.py 8981 2008-08-24 23:51:53Z ceball $
"""
__version__='$Revision: 8981 $'

from topo.base.functionfamily import ResponseFn

# Imported here so that all ResponseFns will be in the same package
from topo.base.cf import DotProduct

__all__ = list(set([k for k,v in locals().items()
                    if isinstance(v,type) and issubclass(v,ResponseFn)]))
