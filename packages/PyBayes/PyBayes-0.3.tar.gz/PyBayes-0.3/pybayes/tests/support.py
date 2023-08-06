# Copyright (c) 2010 Matej Laitl <matej@laitl.cz>
# Distributed under the terms of the GNU General Public License v2 or any
# later version of the license, at your option.

"""Various support methods for tests"""

import unittest as ut

import numpy as np

class PbTestCase(ut.TestCase):
    """Test case that adds some numeric assert functions"""

    def assertApproxEqual(self, X, Y):
        """Return true if X = Y to within machine precision

        Function for checking that different matrices from different
        computations are in some sense "equal" in the verification tests.
        """
        X = np.asarray(X)
        Y = np.asarray(Y)
        fuzz = 1.0e-8

        self.assertEqual(X.ndim, Y.ndim)
        self.assertEqual(X.shape, Y.shape)

        if np.all(abs(X - Y) < fuzz):
            return
        else:
            self.fail("NumPy arrays {0} and {1} are not fuzzy equal (+- {2})".format(X, Y, fuzz))

    def assertArraysEqualNotSame(self, a, b):
        """Assert that numpy arrays a and b are equal, but are not the same instances"""
        self.assertTrue(id(a) != id(b))
        self.assertTrue(a.ndim == b.ndim)
        self.assertTrue(np.all(a == b))

    def assertRVsEqualNotSame(self, a, b):
        """Assert that :class:`~pybayes.pdfs.RV` objects a and b are equal, but
        are not the same instances neither shallow copies of themselves.

        RVs are special case during deepcopy - the RVComps should be referenced,
        not copied."""
        self.assertTrue(id(a) != id(b))
        self.assertTrue(id(a.components) != id(b.components))
        self.assertEqual(a.name, b.name)  # no need to test for id inequality - strings are immutable
        self.assertEqual(a.dimension, b.dimension)  # ditto
        for (a_comp, b_comp) in zip(a.components, b.components):
            # equality for rv comps is defined as object instance identity
            self.assertEqual(a_comp, b_comp)
