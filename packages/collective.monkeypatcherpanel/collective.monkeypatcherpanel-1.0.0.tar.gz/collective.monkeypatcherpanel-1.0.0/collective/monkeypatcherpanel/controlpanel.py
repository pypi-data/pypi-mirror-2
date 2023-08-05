# -*- coding: utf-8 -*-
# $Id: controlpanel.py 113853 2010-03-23 15:43:02Z glenfant $
"""ZMI control panel"""

import Acquisition
import Globals
from OFS import SimpleItem
from App.version_txt import getZopeVersion
version = getZopeVersion()
if version > (2, 12):
    class Fake:
        pass
else:
    from App.ApplicationManager import Fake
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

all_patches = []

def monkeyPatchAdded(event):
    """See collective.monkeypatcher.interfaces.IMonkeyPatchEvent"""
    all_patches.append(event.patch_info)
    return


class ControlPanel(Fake, SimpleItem.Item, Acquisition.Implicit):
    """The Monkey patches control panel"""

    id = 'collective_monkeypatcherpanel'
    name = title = "Monkey Patches"
    meta_type = "Monkey patches control panel"
    icon = 'misc_/collective.monkeypatcherpanel/icon.png'
    manage_main = PageTemplateFile('zmi/controlpanel.pt', globals())

    manage_options=((
        {'label': 'Monkey Patches', 'action': 'manage_main'},
        ))

    def getId(self):
        return self.id

    def allPatches(self):
        return all_patches

Globals.InitializeClass(ControlPanel)
