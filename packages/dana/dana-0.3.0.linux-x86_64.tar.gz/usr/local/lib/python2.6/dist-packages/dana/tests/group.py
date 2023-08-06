#!/usr/bin/env python
#-----------------------------------------------------------------------------
# DANA - Distributed (Asynchronous) Numerical Adaptive computing framework
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import unittest
import numpy as np
from dana import Group


class GroupDefault(unittest.TestCase):
    def setUp(self):
        self.Z = Group()
    def test_shape(self):
        assert self.Z.shape == ()
    def test_dtype(self):
        assert self.Z.dtype == np.dtype([('f0',float),])
    def test_size(self):
        assert self.Z.size == 1
    def test_fieldname(self):
        assert self.Z.f0 == self.Z.f0

class GroupShape(unittest.TestCase):
    def setUp(self):
        self.Z = Group((3,5))
    def test_shape(self):
        assert self.Z.shape == (3,5)
    def test_size(self):
        assert self.Z.size == 15
    def test_len(self):
        assert len(self.Z) == 3


class GroupFill(unittest.TestCase):
    def setUp(self):
        self.Z = Group((3,5), fill=1.2)
    def test_fill(self):
        assert 1-(self.Z.f0-np.ones((3,5))*1.2).all()

class GroupDtype(unittest.TestCase):
    def setUp(self):
        self.Z = Group((5,5), dtype=[('x',float), ('y',float)])
    def test_dtype(self):
        assert self.Z.dtype == np.dtype([('x',float), ('y',float)])
    def test_contiguity(self):
        assert self.Z.x.flags['C_CONTIGUOUS']
        assert self.Z.y.flags['C_CONTIGUOUS']

class GroupAddItem(unittest.TestCase):
    def setUp(self):
        self.Z = Group((5,5), dtype=[('x',float), ('y',float)])
    def test_int(self):
        self.Z['z'] = 1
        assert self.Z.z.shape == (5,5)
        assert self.Z.z.dtype == np.int64
    def test_float(self):
        self.Z['z'] = 1.0
        assert self.Z.z.shape == (5,5)
        assert self.Z.z.dtype == np.float64

class GroupDelItem(unittest.TestCase):
    def setUp(self):
        self.Z = Group((5,5), dtype=[('x',float), ('y',float)])
    def test_del(self):
        del self.Z['y']
        assert self.Z.dtype == np.dtype([('x',float),])

class GroupSetItem(unittest.TestCase):
    def setUp(self):
        self.Z = Group((5,5), dtype=[('U', float), ('V', int)])
    def test_setitem_1(self):
        self.Z[0,0] = 2
        assert self.Z[0,0] == (2,2)
    def test_setitem_2(self):
        self.Z[0,0] = 1,2
        assert self.Z[0,0] == (1,2)
    def test_setitem_3(self):
        self.Z[:,:] = 1,2
        assert self.Z.U.sum() == 1*self.Z.size
        assert self.Z.V.sum() == 2*self.Z.size
    def test_setitem_4(self):
        self.Z[...] = 1,2
        assert self.Z.U.sum() == 1*self.Z.size
        assert self.Z.V.sum() == 2*self.Z.size
    def test_Group_setitem_5(self):
        def _set_(): self.Z[0,0] = 1,2,3
        self.assertRaises(ValueError, _set_)

class GroupGetItem(unittest.TestCase):
    def setUp(self):
        self.Z = Group((5,5), dtype=[('U', float), ('V', int)])
    def test_getitem_1(self):
        a,b = self.Z[0,0]
        assert type(a) is np.float64
        assert type(b) is np.int64
    def test_getitem_2(self):
        assert self.Z[:2,:2].shape == (2,2)
        assert self.Z[:2,:2].dtype == np.dtype([('U', float), ('V', int)])

class GroupReshape(unittest.TestCase):
     def setUp(self):
         self.Z = Group((5,5), dtype=[('x',float), ('y',float)])
     def test_reshape(self):
         Z = self.Z.reshape((25,))
         assert Z.x.base is self.Z.x
         assert Z.y.base is self.Z.y

class GroupSubGroup(unittest.TestCase):
     def setUp(self):
         self.Z = Group((5,5), dtype=[('x',float), ('y',float)])
     def test_subgroup_1(self):
         S = self.Z.subgroup('x')
         assert S.base is self.Z
     def test_subgroup_2(self):
         S = self.Z('x')
         assert S.base is self.Z


class GroupFunctions(unittest.TestCase):
    def test_Group_asarray(self):
        G = Group((5,5), dtype=[('U', float), ('V', int)], fill=1)
        A = G.asarray()
        assert A.shape == (5,5)
        assert A.dtype == np.dtype([('U', float), ('V', int)])
        assert A['U'].sum() == 25
        assert A['V'].sum() == 25

if __name__ == "__main__":
    unittest.main()
    
