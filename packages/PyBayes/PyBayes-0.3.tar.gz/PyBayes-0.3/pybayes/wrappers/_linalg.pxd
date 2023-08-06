# Copyright (c) 2010 Matej Laitl <matej@laitl.cz>
# Distributed under the terms of the GNU General Public License v2 or any
# later version of the license, at your option.

"""Definitions for wrapper around numpy.linalg - cython version"""

from numpy cimport ndarray

cdef ndarray inv(ndarray A)
