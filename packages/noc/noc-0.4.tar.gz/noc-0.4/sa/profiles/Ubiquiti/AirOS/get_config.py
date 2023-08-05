# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Ubiquiti.AirOS.get_config
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
import noc.sa.script
from noc.sa.interfaces import IGetConfig

class Script(noc.sa.script.Script):
    name="Ubiquiti.AirOS.get_config"
    implements=[IGetConfig]
    def execute(self):
        config=self.cli("cat /tmp/system.cfg")
        return self.cleaned_config(config)
