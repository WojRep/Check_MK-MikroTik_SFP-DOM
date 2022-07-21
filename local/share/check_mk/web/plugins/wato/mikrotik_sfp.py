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
#    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)

# register_check_parameters(
#     subgroup_networking,
#     'mikrotik_sfp',
#     _('MikroTik SFP/SFP+'),

def _parameter_valuespec_mikrotik_sfp():
    return Transform(
        Dictionary(
            title=_('MikroTik SFP/SFP+ Params'),
            elements=[
                ('rx', Tuple(
                    title=_('SFP/SFP+ Rx Signal'),
                    elements=[
                        Float(title=_('Warning at'), unit='dBm',
                              default_value='-14', # allow_empty=False
                              ),
                        Float(title=_('Critical at'), unit='dBm',
                              default_value='-18', # allow_empty=False
                              ),
                    ])),
                ('temp', Tuple(
                    title=_('SFP/SFP+ Temperature'),
                    elements=[
                        Float(title=_('Warning at'), unit='st.C',
                              default_value='55.0', # allow_empty=False
                              ),
                        Float(title=_('Critical at'), unit='st.C',
                              default_value='65.0', # allow_empty=False
                              ),
                    ])),
            ], default_value=['rx']
        ),
        forth=lambda old: type(old) != dict and {"rx": old} or old,
    )


def _item_valuespec_mikrotik_sfp():
      return TextAscii(title=_("MikroTik SFP/SFP+"))



rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="mikrotik_sfp",
        group=RulespecGroupCheckParametersNetworking,
        match_type="dict",
        item_spec-_item_valuespec_mikrotik_sfp,
        parameter_valuespec=_parameter_valuespec_tinycontrol_lk3x,
        title=lambda: _("MikroTik SFP/SFP+"),
    )
)


#     TextAscii(
#         title=_("MikroTik SFP/SFP+"),
# #        allow_empty=False,
#     ),
#     match_type='dict',
#     #       match = 'all',
)
#group = "agents/" + _("Agent Plugins")
# register_rule(group,
#   "agent_config:mikrotik_sfp",
#   Alternative(
#     title = _("MikroTik SFP/SFP+),
#     style = 'dropdown',
#     elements = [
#                ('enable_sfp', FixedValue(
#                    'enable_sfp',
#                    title=_('Enable SFP/SFP+ discovery'),
# elements = [
# FixedValue(title=_('Enable'),default_value='0'),
# ]
#                    ),),]
#     )
#   )
