#
# PyNetlist is an open source framework
# for object-oriented electronic circuit synthesis,
# published under the MIT License (MIT).
#
# Copyright (c) 2015 Jonathan Binas
#

from base import *


class Circuit(Device):
    '''Container for the whole circuit'''
    def parseargs(self, **kwargs):
        for key,val in kwargs.items():
            if isinstance(val, Net) and key not in self.ports:
                self.ports.append(key)
            if isinstance(val, Param) and key not in self.params:
                self.params.append(key)
        super(Circuit, self).parseargs(**kwargs)

    def post_init(self, **kwargs):
        import interfaces
        self.devices = {}
        self.nets = set()
        self.parameters = set()
        self.maxid = 0
        self.maxid_nets = 0
        self.maxid_params = 0
        self.header = ''
        self.footer = ''
        for p in self._params: #index parameters
            self.add(p)
        class Subcircuit(Device):
            circuit = self
            ports = self.ports
            params = self.params
            name = self.name
        self.Instance = Subcircuit

    def add(self, obj):
        '''Add single device instances to the circuit'''
        if obj.type is Circuit:
            for n in obj.nets:
                self.add(n)
            for dgroup in obj.devices.values():
                for d in dgroup:
                    self.add(d)
            return obj
        elif obj.type is Net:
            if obj.globalnet == True:
                return #ignore global nets
            if obj not in self.nets:
                obj.id = self.maxid_nets + 1
                self.nets.add(obj)
                self.maxid_nets = obj.id
                return obj
        elif obj.type is Param:
            if obj not in self.parameters:
                obj.id = self.maxid_params + 1
                self.parameters.add(obj)
                self.maxid_params = obj.id
                return obj
        else: #obj is device
            if obj.type not in self.devices:
                self.devices[obj.type] = set()
            devlist = self.devices[obj.type]
            if obj not in devlist:
                for p in obj._ports + obj._params:
                    self.add(p)
                obj.id = self.maxid + 1
                devlist.add(obj)
                self.maxid = obj.id
                return obj
        return False

    def addArray(self, D, size=1, **kwargs):
        '''Add an array of device instances of class D to the circuit
           If dimensions match, ports are handled automatically'''
        devices = []
        for i in xrange(size):
            kwargs_new = {}
            for key,val in kwargs.items():
                if isinstance(val, (PortList, ParamList)):
                    if len(val)==size:
                        kwargs_new[key] = val[i]
                    else:
                        raise ValueError('Dimension mismatch: %s.%s (%s, %s)' % (D.__name__, key, len(val), size))
                else:
                    kwargs_new[key] = val
            devices.append(self.addNode(D, **kwargs_new))
        return DeviceList(devices)

    def addNode(self, D, **kwargs):
        return self.add(D(**kwargs))
