#!/usr/bin/env python

"""Unit tests for supercell.py
"""

# version
__id__ = '$Id: TestSuperCell.py 2780 2009-02-26 20:17:11Z juhas $'

import os
import unittest

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

from matter import Structure
from matter.expansion import supercell


##############################################################################
class TestSuperCell(unittest.TestCase):

    stru_cdse = None
    stru_ni = None

    def setUp(self):
        # load test structures once
        if TestSuperCell.stru_cdse is None:
            cdsefile = os.path.join(testdata_dir, "CdSe_bulk.stru")
            TestSuperCell.stru_cdse = Structure(filename=cdsefile)
        if TestSuperCell.stru_ni is None:
            nifile = os.path.join(testdata_dir, "Ni.stru")
            TestSuperCell.stru_ni = Structure(filename=nifile)
        # bring them to the instance
        self.stru_cdse = TestSuperCell.stru_cdse
        self.stru_ni = TestSuperCell.stru_ni
        return

    def tearDown(self):
        return

    def test_exceptions(self):
        """check argument checking of supercell.
        """
        self.assertRaises(ValueError,
                supercell, self.stru_ni, (0, 1, 1))
        self.assertRaises(ValueError,
                supercell, self.stru_ni, (0, 1))
        self.assertRaises(TypeError,
                supercell, list(self.stru_ni), (1, 1, 1))
        return

    def test_ni_supercell(self):
        """check supercell expansion for Ni.
        """
        ni_123 = supercell(self.stru_ni, (1, 2, 3))
        self.assertEqual(6*len(self.stru_ni), len(ni_123))
        a, b, c = self.stru_ni.lattice.abcABG()[:3]
        a1, b2, c3 = ni_123.lattice.abcABG()[:3]
        self.assertAlmostEqual(a, a1, 8)
        self.assertAlmostEqual(b*2, b2, 8)
        self.assertAlmostEqual(c*3, c3, 8)
        x, y, z = self.stru_ni[-1].xyz
        x1, y2, z3 = ni_123[-1*2*3].xyz
        self.assertAlmostEqual(x/1, x1, 8)
        self.assertAlmostEqual(y/2, y2, 8)
        self.assertAlmostEqual(z/3, z3, 8)
        return

    def test_cdse_supercell(self):
        """check supercell expansion for CdSe.
        """
        cdse_222 = supercell(self.stru_cdse, (2, 2, 2))
        # new atoms should be grouped together
        elems = sum([8*[a.symbol] for a in self.stru_cdse], [])
        elems_222 = [a.symbol for a in cdse_222]
        self.assertEqual(elems, elems_222)
        return

# End of class TestRoutines


if __name__ == '__main__':
    unittest.main()

# End of file
