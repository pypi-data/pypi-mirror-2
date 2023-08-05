"""

$Id: testoutputfnsoptimized.py 7458 2007-12-29 13:10:02Z ceball $
"""
__version__='$Revision: 7458 $'

# CEBHACKALERT: we should delete this file, right?

import unittest

from numpy.oldnumeric import array, Float32

# Currently empty; should be expanded
cases = []

suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(case) for case in cases)
              
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite)
    


        
