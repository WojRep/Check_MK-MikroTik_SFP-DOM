#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.plugins.views.perfometers import (
    perfometer_linear,
    perfometer_logarithmic,
    perfometer_logarithmic_dual,
    perfometer_logarithmic_dual_independent,
)

from math import fabs

def perfometer_mikrotik_sfp(row, check_command, perf_data):
    for perf in perf_data:
        perf = list(perf)
        rx_power = float(perf[1]) if perf[0] == 'rx_power' else -40.0 
        sfp_temp = float(perf[1]) if perf[0] == 'sfp_temp' else 0.0
    return u"%s&nbsp;&nbsp;/&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;&nbsp;" % (str('{0: .1f}'.format(rx_power)) + 'dBm', str('{0: .0f}'.format(sfp_temp)) + '°C'), perfometer_logarithmic_dual_independent(fabs(rx_power), '#54b948', 10, 2,
                                                                        fabs(sfp_temp), '#2098cb', 35, 2)

perfometers['check_mk-mikrotik_sfp'] = perfometer_mikrotik_sfp
