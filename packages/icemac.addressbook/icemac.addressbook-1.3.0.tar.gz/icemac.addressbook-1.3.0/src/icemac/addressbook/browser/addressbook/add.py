# -*- coding: latin-1 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt
# $Id: add.py 783 2010-01-09 14:28:06Z icemac $

import icemac.addressbook.interfaces
import icemac.addressbook.browser.base
import icemac.addressbook.addressbook
from icemac.addressbook.i18n import MessageFactory as _


class AddForm(icemac.addressbook.browser.base.BaseAddForm):
    
    label = _(u'Add new address book')
    interface = icemac.addressbook.interfaces.IAddressBook
    class_ = icemac.addressbook.addressbook.AddressBook
    next_url = 'object'
