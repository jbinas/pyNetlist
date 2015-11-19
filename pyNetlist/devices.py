#
# PyNetlist is an open source framework
# for object-oriented electronic circuit synthesis,
# published under the MIT License (MIT).
#
# Copyright (c) 2015 Jonathan Binas
#

from base import Net, Device


class V(Device):
    ports = ['p1', 'p2']
    params = ['v']


class I(Device):
    ports = ['p1', 'p2']
    params = ['i']


class R(Device):
    ports = ['p1', 'p2']
    params = ['r']


class C(Device):
    ports = ['p1', 'p2']
    params = ['c']


class NMOS(Device):
    name = 'M'
    ports = ['d', 'g', 's', 'b']
    params = ['model', 'l', 'w', 'm', 'delvto']


class PMOS(Device):
    name = 'M'
    ports = ['d', 'g', 's', 'b']
    params = ['model', 'l', 'w', 'm', 'delvto']

