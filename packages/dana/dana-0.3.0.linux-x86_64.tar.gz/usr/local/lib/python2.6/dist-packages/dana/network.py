#!/usr/bin/env python
# -----------------------------------------------------------------------------
# DANA - Distributed (Asynchronous) Numerical Adaptive computing framework
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
# -----------------------------------------------------------------------------

class NetworkError(Exception):
    pass

class Network(object):

    def __init__(self, groups=[]):
        self._groups = groups

    def run(self, t=1.0, dt=0.01, n=None, asynchrony_level=0):
        ''' '''

        if n == None:
            n = int(t/dt)
        else:
            dt = 1
        for group in self._groups:
            group.setup()
        for i in range(n):
            for group in self._groups:
                group.evaluate(dt=dt, asynchrony_level=asynchrony_level)

    def append(self, group):
        ''' '''
        if group not in self._groups:
            self._groups.append(group)
        else:
            raise NetworkError, 'Group is already in network'

__default_network__ = Network([])

def run(t=1.0, dt=0.01, n=None):
    __default_network__.run(t,dt,n)
