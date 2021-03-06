#
# PyNetlist is an open source framework
# for object-oriented electronic circuit synthesis,
# published under the MIT License (MIT).
#
# Copyright (c) 2015 Jonathan Binas
#


from pyNetlist.base import *


def netlist(circuit, dynamic_params=False, use_subckt_ref=False):
    '''spice netlist generator'''
    out = ''
    subckts = []
    devtypes = sorted(circuit.devices, key=lambda k: (k.__name__, k.name))
    for devtype in devtypes:
        for dev in sorted(circuit.devices[devtype], key=lambda k: k.id):
            ref_prefix = ''
            params = []
            is_subckt = True if dev.__class__.__name__=='Subcircuit' else False
            #TODO: find better way of testing for subcircuit
            if is_subckt:
                if dev.circuit not in subckts:
                    subckts.append(dev.circuit)
                if dev.ref[0] not in ['x','X']:
                    ref_prefix = 'X'
                params.append(dev.circuit.ref)
            ref = [ref_prefix + dev.ref]
            ports = [p.ref for p in dev._ports]
            for p in dev.params:
                prefix = ''
                if is_subckt and use_subckt_ref:
                    prefix += dev.circuit.ref + '_'
                if len(params):
                    prefix += p + '='
                if dynamic_params and dev[p] in circuit._params:
                    #use supercircuit param names
                    ckt_ref = circuit.ref + '_' if use_subckt_ref else ''
                    param = prefix + ckt_ref + \
                            circuit.params[circuit._params.index(dev[p])]
                    params.append(param)
                elif dev[p].value is not None:
                    #optional parameters
                    params.append(prefix + str(dev[p].value))
                elif len(params) == 0:
                    #device value must be present
                    params.append(prefix + 'NULL')
            out += ' '.join(ref + ports + params) + '\n'
    for c in subckts:
        #generate subcircuits
        ports = [p.ref for p in c._ports]
        params = []
        for p in c.params:
            value = c[p].value if c[p].value is not None else 'NULL'
            ckt_ref = c.ref + '_' if use_subckt_ref else ''
            params.append(ckt_ref + p + '=' + str(value))
        out += '.subckt %s ' % c.ref
        out += ' '.join(ports + params) + '\n'
        out += netlist(c, dynamic_params=True, use_subckt_ref=use_subckt_ref)
        out += '.ends %s\n' % c.ref
    return out

def comment(text):
    return '* %s\n' % text

def command(cmd, *args):
    return '.%s %s\n' % (cmd, ' '.join(
        [arg.ref if isinstance(arg, Device) else str(arg) for arg in args]))

def wrdata(filename, fct, nodes):
    if isinstance(nodes, Device):
        nodes = [nodes]
    fcts = ' '.join([fct+'('+n.ref+')' for n in nodes])
    return command('wrdata', filename, fcts)[1:]

def include(filename):
    return command('inc', filename)

def dc(*args):
    return command('dc', *args)[1:]

