# -*- coding: latin-1 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt
# $Id: evolve4.py 783 2010-01-09 14:28:06Z icemac $

__docformat__ = "reStructuredText"

import zope.app.generations.utility


generation = 4


def evolve(context):
    """Update the root folder to be a ``zope.site.folder.Folder`` instead of
       ``zope.app.folder.folder.Folder``.
    """
    root = zope.app.generations.utility.getRootFolder(context)
    context.connection.root()._p_changed = True
    root._p_changed = True
