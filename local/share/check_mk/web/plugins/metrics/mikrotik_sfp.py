#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    check_metrics,
    metric_info,
    graph_info,
)

metric_info['rx_power'] = {
    'title': _(' Optical Rx signal power'),
    'unit' :'dbm',
    'color': '24/a',
}

metric_info['tx_power'] = {
    'title': _('Opticam Tx signal power'),
    'unit': 'dbm',
    'color': '15/b',
}

metric_info['sfp_temp'] = {
    'title': _('Temperature'),
    'unit': 'c',
    'color': '46/b',
}

metric_info['sfp_voltage'] = {
    'title': _('Voltage'),
    'unit': 'v',
    'color': '34/a',
}

unit_info["ma"] = {
    "title": _("BIAS Current"),
    "symbol": _("mA"),
    "render": lambda v: cmk.utils.render.physical_precision(v, 3, _("mA")),
    "js_render": "v => cmk.number_format.physical_precision(v, 3, 'mA')",
}

metric_info['bias'] = {
    'title': _('Bias current'),
    'unit': 'ma',
    'color': '31/b',
}

