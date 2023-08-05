# -*- coding: latin-1 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt
# $Id: evolve7.py 783 2010-01-09 14:28:06Z icemac $

__docformat__ = "reStructuredText"


import icemac.addressbook.generations.utils


generation = 7


def evolve(context):
    """Install user defined fields utility.
    """
    icemac.addressbook.generations.utils.update_address_book_infrastructure(
        context)

