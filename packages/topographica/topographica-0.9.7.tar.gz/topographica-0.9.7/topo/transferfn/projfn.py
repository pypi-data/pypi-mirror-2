"""
Output functions (see basic.py) that apply to a whole Projection. For
example, for a CFProjection this involves iterating through all the
CFs and applying an output function to each set of weights in turn.

$Id: projfn.py 9831 2009-01-25 16:34:35Z ceball $
"""
__version__='$Revision: 9831 $'

from topo.base.cf import CFPOutputFn

# imported here so that all projection-level output functions are in the
# same package
from topo.base.cf import CFPOF_Plugin,CFPOF_Identity



__all__ = list(set([k for k,v in locals().items() if isinstance(v,type) and issubclass(v,CFPOutputFn)]))

