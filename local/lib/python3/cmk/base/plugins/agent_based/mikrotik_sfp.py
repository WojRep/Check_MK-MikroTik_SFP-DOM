#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
from .agent_based_api.v1 import *

from .agent_based_api.v1.type_defs import *

from .utils import (
    temperature,
)

from typing import Dict, List

from cmk.utils import debug
from pprint import pprint

def _isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def _isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

UNIT = {
    "c": u"°C",
    'v': u"V",
    'a': u"A",
    'w': u"W",
    'dbm': u"dBm",
    '%': u"%",
}

def _render_template(value: float):
    template = "%%%s" % ("d" if isinstance(value, int) else ".1f")
    return template % value


def _render_func(value: float, unit: str) -> str:
    return _render_template(value) + UNIT.get(unit) if UNIT.get(unit) else ''



#factory_settings["mikrotik_sfp_default_levels"] = {
#    'rx': (-15.0, -22.0),
#    'temp': (55.0, 65.0),
#}

SNMP_BASE = '.1.3.6.1.4.1.14988.1.1.19.1.1'

SNMP_DETECT = exists('.1.3.6.1.4.1.14988.1.1.19.1.1')


OIDs = [
    {'id': '_', 'oid': OIDEnd() , },
    {'id': 'if_name', 'oid': '2', 'do_metric': False, },  # SFP interface name
    {'id': 'wave_length', 'oid': '5', 'do_metric': False, 'unit': 'nm', 'divider': 100, },  # Wave Length
    {'id': 'temp', 'oid': '6', 'do_metric': True, 'unit': 'c', 'divider': 1000, },  # SFP Temp
    {'id': 'voltage', 'oid': '7', 'do_metric': True, 'unit': 'v', 'divider': 1000, },  # SFP Supply Voltage
    {'id': 'bias', 'oid': '8', 'do_metric': True, 'unit': 'a', 'divider': 1000, },  # SFP Bias Current
    {'id': 'tx_power', 'oid': '9', 'do_metric': True, 'unit': 'dbm', 'divider': 100, },  # FTP Optical Tx
    {'id': 'rx_power', 'oid': '10', 'do_metric': True, 'unit': 'dbm', 'divider': 100, },  # SFP Oprical Rx
    {'id': 'mtxrOpticalTxFault', 'oid': '4', 'do_metric': False, },  # mtxrOpticalTxFault
    {'id': 'vendor', 'oid': '11', 'do_metric': False, }, # Vendor
]

def parse_mikrotik_sfp(string_table):

    pprint('########## string_table ############')
    pprint(string_table)
    pprint('####################################')

    interface_list = []
    for m in range(len(string_table)):
        parameters = string_table[m]
        for n in range(len(parameters)):
            divider =  OIDs[n].get('divider') if OIDs[n].get('divider') else 1
            if _isInt(parameters[n]) and divider == 1:
                value = int(parameters[n])
            elif _isFloat(parameters[n]):
                value = float(int(parameters[n]) / divider)
            else:
                value = str(parameters[n])
                if (value is None) or (value == ''):
                    value = chr(216)
            parameters[n] = value
        interface_list.append(parameters)

    pprint('#### interface_list ####')
    pprint(interface_list)
    pprint('########################')
    return interface_list

def discover_mikrotik_sfp(section):
    pprint('#### section ####')
    pprint(section)
    pprint('#################')

    for line in section:
        if len(line) > 0:
            yield Service(item=line[1])


def check_mikrotik_sfp(item, params, section):
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data")
        return

    state = State.OK
    summary = None
    notice = None
    details = ""

    pass

register.snmp_section(
    name='mikrotik_sfp',
    fetch = SNMPTree(
        base = SNMP_BASE,
        oids = [ oid['oid'] for oid in OIDs],
    ),
    detect = SNMP_DETECT,
    parse_function = parse_mikrotik_sfp,
)


register.check_plugin(
    name = 'mikrotik_sfp',
    sections=['mikrotik_sfp'],
    service_name = "SFP params - %s",
    discovery_function = discover_mikrotik_sfp,
    check_default_parameters={},
    check_ruleset_name='mikrotik_sfp',
    check_function = check_mikrotik_sfp,
)