# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt
# $Id: __init__.py 865 2010-03-07 15:52:31Z icemac $
"""Database initialisation and upgrading."""

import zope.app.generations.generations


GENERATION = 9


manager = zope.app.generations.generations.SchemaManager(
    minimum_generation=GENERATION,
    generation=GENERATION,
    package_name='icemac.addressbook.generations')
