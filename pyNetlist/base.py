#
# PyNetlist is an open source framework
# for object-oriented electronic circuit synthesis,
# published under the MIT License (MIT).
#
# Copyright (c) 2015 Jonathan Binas
#

class BaseObj(object):
    '''Base class for devices and nets'''
    name = None
    def __init__(self, *args, **kwargs):
        self.type = self.__class__
        if self.name is None:
            self.name = self.__class__.__name__
        self.id = None
        self.parseargs(*args, **kwargs)
        self.post_init(*args, **kwargs)

    def post_init(self, *args, **kwargs):
        pass

    def parseargs(self, *args, **kwargs):
        pass

    def get_ref(self):
        if self.id is None:
            id = ''
        else:
            id = str(self.id)
        return self.name + id

    @property
    def ref(self):
        return self.get_ref()


class BaseObjList(object):
    '''Base class for lists of devices, ports, params...'''
    def __init__(self, arr):
        self.elements = arr

    def __len__(self):
        return self.elements.__len__()

    def __iter__(self):
        return self.elements.__iter__()

    def __getitem__(self, val):
        return self.elements[val]


class DeviceList(BaseObjList):
    '''Contains an array of devices of a specific type'''
    def __getattr__(self, port_id):
        return PortList([d[port_id] for d in self.elements])


class PortList(BaseObjList):
    pass


class ParamList(BaseObjList):
    pass


class Device(BaseObj):
    '''Device base class'''
    ports = []
    params = []

    def parseargs(self, **kwargs):
        self.ports = kwargs.pop('ports', self.ports)
        self.params = kwargs.pop('params', self.params)
        self.name = kwargs.get('name', self.name)
        self._ports = [kwargs.get(id, Net()) for id in self.ports]
        self._params = []
        for id in self.params:
            val = kwargs.get(id, None)
            if isinstance(val, Param):
                self._params.append(val)
            else:
                self._params.append(Param(val))
        for i, port_id in enumerate(self.ports):
            links = self._ports[i].links
            if self not in links:
                links[self] = [port_id]
            elif port_id not in links[self]:
                links[self].append(port_id)

    def __getitem__(self, id):
        if id in self.ports:
            return self._ports[self.ports.index(id)]
        elif id in self.params:
            return self._params[self.params.index(id)]
        else:
            raise AttributeError('This port does not exist: %s' % id)

    def __getattr__(self, id):
        return self.__getitem__(id)


class Net(BaseObj):
    def post_init(self, **kwargs):
        self.name = kwargs.get('name', 'N')
        self.globalnet = kwargs.get('globalnet', False)
        self.links = {}


class Param(BaseObj):
    def parseargs(self, value=None):
        self.value = value
