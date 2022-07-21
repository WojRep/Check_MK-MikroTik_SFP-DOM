#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _

from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
    TextAscii,
    Checkbox,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)


def _parameter_valuespec_mikrotik_sfp():
    return Transform(
        Dictionary(
            title=_('MikroTik SFP/SFP+ Params'),
            elements=[
                ('rx_power', Tuple(
                    title=_('SFP/SFP+ Rx Signal'),
                    elements=[
                        Float(title=_('Warning at'), unit='dBm',
                              default_value='-14.0',
                              ),
                        Float(title=_('Critical at'), unit='dBm',
                              default_value='-18.0',
                              ),
                    ])),
                ('tx_power_lower', Tuple(
                    title=_('SFP/SFP+ Lower Tx Signal'),
                    elements=[
                        Float(title=_('Warning at'), unit='dBm',
                              default_value='-10.0',
                              ),
                        Float(title=_('Critical at'), unit='dBm',
                              default_value='-12.0',
                              ),
                    ])),
                ('tx_power_upper', Tuple(
                    title=_('SFP/SFP+ Upper Tx Signal'),
                    elements=[
                        Float(title=_('Warning at'), unit='dBm',
                              default_value='-2.0',
                              ),
                        Float(title=_('Critical at'), unit='dBm',
                              default_value='-1.0',
                              ),
                    ])),
                ('temp', Tuple(
                    title=_('SFP/SFP+ Temperature'),
                    elements=[
                        Float(title=_('Warning at'), unit='st.C',
                              default_value='55.0', 
                              ),
                        Float(title=_('Critical at'), unit='st.C',
                              default_value='65.0', 
                              ),
                    ])),
            ], 
        ),
    )


def _item_valuespec_mikrotik_sfp():
      return TextAscii(title=_("MikroTik SFP/SFP+"))



rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mikrotik_sfp",
        group=RulespecGroupCheckParametersNetworking,
        match_type="dict",
        item_spec=_item_valuespec_mikrotik_sfp,
        parameter_valuespec=_parameter_valuespec_mikrotik_sfp,
        title=lambda: _("MikroTik SFP/SFP+"),
    )
)
