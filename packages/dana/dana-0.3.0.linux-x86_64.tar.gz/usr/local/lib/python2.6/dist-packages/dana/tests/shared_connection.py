#!/usr/bin/env python
# -----------------------------------------------------------------------------
# DANA - Distributed (Asynchronous) Numerical Adaptive computing framework
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
# -----------------------------------------------------------------------------
import unittest
from numpy import *
import scipy.sparse as sp
from tools import np_equal
from dana import ConnectionError
from dana import SharedConnection as Connection

class SharedOneDimensionTestCase(unittest.TestCase):

    def test_1(self):
        assert np_equal( Connection(ones(3), ones(3), ones(1)).output(),
                         ones(3))

    def test_2(self):
        self.assertRaises(ConnectionError,
                          Connection, ones(3), ones(5), ones(1))

    def test_3(self):
        assert np_equal( Connection(ones(3), ones(3), ones(3)).output(),
                         array([2,3,2]))

    def test_4(self):
        assert np_equal( Connection(ones(3), ones(3), array([1,NaN,1])).output(),
                         array([1,2,1]))

    def test_5(self):
        assert np_equal( Connection(ones(3), ones(3), array([NaN,NaN,NaN])).output(),
                         zeros(3))

    def test_6(self):
        self.assertRaises(ConnectionError,
                          Connection, ones(3), ones(3), ones((3,3)))

    def test_7(self):
        C = Connection(ones(3), ones(3), ones(1))
        assert np_equal(C[0], array([1, NaN, NaN]))
        assert np_equal(C[1], array([NaN, 1, NaN]))
        assert np_equal(C[2], array([NaN, NaN, 1]))



class SharedTwoDimensionTestCase(unittest.TestCase):

    def test_1(self):
        assert np_equal( Connection(ones((3,3)), ones((3,3)), ones((1,1))).output(),
                         ones((3,3)))
    def test_2(self):
        assert np_equal( Connection(ones((3,3)), ones((3,3)), ones((3,3))).output(),
                         array([[4,6,4],
                                [6,9,6],
                                [4,6,4]]))
    def test_3(self):
        assert np_equal( Connection(ones((3,3)), ones((3,3)), array([[1, 1, 1],
                                                                     [1,NaN,1],
                                                                     [1, 1, 1]])).output(),
                         array([[3,5,3],
                                [5,8,5],
                                [3,5,3]]))
    def test_4(self):
        assert np_equal( Connection(ones((3,3)), ones((3,3)), ones((3,3))*NaN).output(),
                         zeros((3,3)) )

    def test_5(self):
        C = Connection(ones((3,3)), ones((3,3)), ones((1,1)))
        assert np_equal(C[1,1], array([[NaN, NaN, NaN],
                                       [NaN,  1,  NaN],
                                       [NaN, NaN, NaN]]))

if __name__ == "__main__":
    unittest.main()
