#!/usr/bin/env python3

register_check_parameters(
    subgroup_networking,
    'mikrotik_sfp',
    _('MikroTik SFP/SFP+'),
    Transform(
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
    ),
    TextAscii(
        title=_("MikroTik SFP/SFP+"),
#        allow_empty=False,
    ),
    match_type='dict',
    #       match = 'all',
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
