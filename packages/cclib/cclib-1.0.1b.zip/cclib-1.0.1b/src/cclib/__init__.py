"""
cclib (http://cclib.sf.net) is (c) 2006-2010, the cclib development team
and licensed under the LGPL (http://www.gnu.org/copyleft/lgpl.html).
"""

__revision__ = "$Revision: 929 $"
__version__ = "1.0.1b"

import parser
import progress
import method
import bridge

# The test module can be imported if it was installed with cclib.
try:
    import test
except:
    pass
