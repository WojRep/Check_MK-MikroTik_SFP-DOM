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
    'ma': u"mA",
    'w': u"W",
    'dbm': u"dBm",
    '%': u"%",
}

def _render_template(value: float):
    template = "%%%s" % ("d" if isinstance(value, int) else ".1f")
    return template % value


def _render_func(value: float, unit: str) -> str:
    return _render_template(value) + UNIT.get(unit) if UNIT.get(unit) else ''

LOSS = {
'0': {'name': 'Signal OK', 'status': State.OK, },
'1': {'name': 'Signal LOSS', 'status': State.CRIT, },
'2': {'name': 'null data', 'status': State.UNKNOWN, },
}


SNMP_BASE = '.1.3.6.1.4.1.14988.1.1.19.1.1'

SNMP_DETECT = startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.14988.1')


OIDs = [
    {'id': '_', 'oid': OIDEnd() , },
    {'id': 'if_name', 'oid': '2', 'long_name': 'SFP Name', 'do_metric': False, },  # SFP interface name
    {'id': 'vendor', 'oid': '11', 'long_name': 'Vendor', 'do_metric': False, }, # Vendor
    {'id': 'wave_length', 'oid': '5', 'long_name': 'Wave Length', 'name': 'Wave', 'do_metric': False, 'unit': 'nm', 'divider': 100, },  # Wave Length
    {'id': 'sfp_temp', 'oid': '6', 'long_name': 'Temperature', 'name': 'Temp', 'do_metric': True, 'unit': 'c', 'divider': 1, 'boundaries': (-5, 100), },  # SFP Temp
    {'id': 'sfp_voltage', 'oid': '7', 'long_name': 'Supply Voltage', 'name': 'Voltage',  'do_metric': True, 'unit': 'v', 'divider': 1000, 'boundaries': (1,5), },  # SFP Supply Voltage
    {'id': 'bias', 'oid': '8', 'long_name': 'Bias Current', 'name': 'Bias', 'do_metric': True, 'unit': 'ma', 'divider': 1 },  # SFP Bias Current
    {'id': 'tx_power', 'oid': '9', 'long_name': 'Tx power', 'name': 'Tx', 'do_metric': True, 'unit': 'dbm', 'divider': 1000, 'boundaries': (-40, 0), },  # FTP Optical Tx
    {'id': 'rx_power', 'oid': '10', 'long_name': 'Rx power', 'name': 'Rx', 'do_metric': True, 'unit': 'dbm', 'divider': 1000, 'boundaries': (-40, 0), },  # SFP Oprical Rx
    {'id': 'mtxrOpticalRxLoss', 'oid': '3', 'long_name': 'Optical Rx', 'do_metric': False, 'alarm': LOSS, },
    {'id': 'mtxrOpticalTxFault', 'oid': '4', 'long_name': 'Optical Tx', 'do_metric': False, 'alarm': LOSS, },
]

def parse_mikrotik_sfp(string_table):
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
    return interface_list

def discover_mikrotik_sfp(section):
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
    for line in section:
        if line[1] == item:
            for n in range(1,len(line)):
                param = OIDs[n].get('id')
                long_name = OIDs[n].get('long_name') if OIDs[n].get('long_name') else param
                name = OIDs[n].get('name') if OIDs[n].get('name') else long_name
                do_metric = OIDs[n].get('do_metric') if OIDs[n].get('do_metric') else False
                unit = OIDs[n].get('unit') if OIDs[n].get('unit') else ''
                boundaries = OIDs[n].get('boundaries') if OIDs[n].get('boundaries') else None
                value = line[n]
                if (param == 'vendor'):
                    vendor = line[n]
                    if (vendor is None) or (vendor == ""):
                        vendor = "?"
                if (param == 'rx_power'):
                    if (value < -33.5) or (value == 0.0):
                       value = -40.0
                if OIDs[n].get('alarm'):
                    value_name = OIDs[n].get('alarm').get(str(value)).get('name')
                    status = OIDs[n].get('alarm').get(str(value)).get('status')
                    details = f"{long_name}: {value_name}{unit}"
                    summary = f"{name}: {value_name}{unit}"
                else:
                    details = f"{long_name}: {value}{unit}"
                    summary = f"{name}: {value}{unit}"
                if param == 'rx_power':
                    lower_levels = params.get('rx_power')
                    upper_levels = (None, None)
                elif param == 'tx_power':
                    lower_levels = params.get('tx_power_lower')
                    upper_levels = params.get('tx_power_upper')
                elif param == 'temp':
                    lower_levels = (None, None)
                    upper_levels = params.get('temp')                
                else:
                    lower_levels = (None, None)
                    upper_levels = (None, None)
                if do_metric and not OIDs[n].get('alarm'):
                    yield from check_levels(
                                value=value,
                                metric_name = param,
                                label = name,
                                levels_upper = upper_levels,
                                levels_lower = lower_levels,
                                render_func = lambda value: _render_func(value, unit),
                                boundaries = boundaries,
                    )
                elif do_metric and OIDs[n].get('alarm'):
                    yield Metric(param, value, boundaries=boundaries)
                    yield Result(state=state, details=details, summary=summary)
                else:
                    yield Result(state=state, details=details, summary=summary)                                   
            return
    yield Result(state=State.UNKNOWN, summary="No item or data")
    return



def inventory_mikrotik_sfp(section):
    for sfp in section:
        yield TableRow(
                 path=["networking","optical_inserts"],
                 key_columns={'Index': sfp[0]},
                 inventory_columns={
                     "Interface": sfp[1],
                     "Vendor": sfp[2],
                     "Wave Lengh": str(sfp[3]),
                 },
              )

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
    check_default_parameters={'rx_power': (-10.0, -25.0), 'temp': (45.0, 65.0), 'tx_power_lower': (-10.0, -12.0), 'tx_power_upper': (-2.0, -1.0), },
    check_ruleset_name='mikrotik_sfp',
    check_function = check_mikrotik_sfp,
)


register.inventory_plugin(
    name = 'inventory_mikrotik_sfp',
    sections=["mikrotik_sfp"],
    inventory_function=inventory_mikrotik_sfp,
)
