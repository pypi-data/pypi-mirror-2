# -*- coding: utf-8 -*-

import grok
import dolmen.content

from dolmen.app.content import icon
from dolmen.app.viewselector import IViewSelector
from menhir.contenttype.folder import MCFMessageFactory as _


class IFolder(IViewSelector):
    """Marker interface for folders.
    """


class Folder(dolmen.content.OrderedContainer):
    icon('folder.png')
    grok.implements(IFolder)
    dolmen.content.name(_(u"Folder"))
    selected_view = "folderlisting"
