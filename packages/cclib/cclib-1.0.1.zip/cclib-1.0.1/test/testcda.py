"""
cclib (http://cclib.sf.net) is (c) 2006, the cclib development team
and licensed under the LGPL (http://www.gnu.org/copyleft/lgpl.html).
"""

__revision__ = "$Rev: 733 $"

import os
import logging
import unittest

# If numpy is not installed, try to import Numeric instead.
try:
    import numpy
except ImportError:
    import Numeric as numpy

from testall import getfile
from cclib.method import CDA
from cclib.parser import Gaussian


def main(log=True):
    data1, logfile1 = getfile(Gaussian, "CDA", "BH3CO-sp.log")
    data2, logfile2 = getfile(Gaussian, "CDA", "BH3.log")
    data3, logfile3 = getfile(Gaussian, "CDA", "CO.log")
    fa = CDA(data1)
    if not log:
        fa.logger.setLevel(logging.ERROR)
    fa.calculate([data2, data3])

    return fa

def printResults():
    fa = main()

    print "       d       b       r"
    print "---------------------------"

    spin = 0
    for i in range(len(fa.donations[0])):

        print "%2i: %7.3f %7.3f %7.3f"%(i,fa.donations[spin][i], fa.bdonations[spin][i], \
                                        fa.repulsions[spin][i])
            

    print "---------------------------"
    print "T:  %7.3f %7.3f %7.3f"%(reduce(numpy.add, fa.donations[0]), \
                reduce(numpy.add, fa.bdonations[0]), reduce(numpy.add, fa.repulsions[0]))
    print "\n\n"

class CDATest(unittest.TestCase):
    def runTest(self):
        """Testing CDA results against Frenking's code"""
        fa = main(log=False)
        
        donation = reduce(numpy.add, fa.donations[0])
        bdonation = reduce(numpy.add, fa.bdonations[0])
        repulsion = reduce(numpy.add, fa.repulsions[0])

        self.assertAlmostEqual(donation, 0.181, 3)
        self.assertAlmostEqual(bdonation, 0.471, 3)
        self.assertAlmostEqual(repulsion, -0.334, 3)


tests = [CDATest]

        
if __name__ == "__main__":
    printResults()
    unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(CDATest))
