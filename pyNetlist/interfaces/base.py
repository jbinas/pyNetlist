#
# PyNetlist is an open source framework
# for object-oriented electrical circuit synthesis,
# published under the MIT License (MIT).
#
# Copyright (c) 2015 Jonathan Binas
#


class File(object):
    def __init__(self, filename=None):
        self.data = ''
	self.filename = filename

    def append(self, string):
        if not isinstance(string, str):
	    raise TypeError('Only strings allowed.')
        self.data += string

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.__repr__()

    def save(self, filename=None):
        if filename is not None:
	    self.filename = filename
	if self.filename is None:
	    raise ValueError('No filename specified.')
	pass
        #TODO: save data...
