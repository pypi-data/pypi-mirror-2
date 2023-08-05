##############################################################################
#
# Copyright (c) 2002-2006 Zope Corporation and Contributors.
# All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
# 
##############################################################################

__doc__='''Package wrapper for Queued Catalogs

$Id: __init__.py 86693 2008-05-13 10:38:43Z andreasjung $'''
__version__='$$'[11:-2]

# Placeholder for Zope Product data
misc_ = {}

from Globals import DTMLFile
from QueueCatalog import QueueCatalog

manage_addQueueCatalogForm = DTMLFile('dtml/add', globals())

def manage_addQueueCatalog(self, id, title='', location=None, REQUEST=None):
    "Add a Catalog Queue"
    ob = QueueCatalog()
    ob.id = id
    ob.manage_edit(title, location, immediate_removal=1)
    self._setObject(id, ob)

    if REQUEST is not None:
        try:
            u = self.DestinationURL()
        except AttributeError:
            u = REQUEST['URL1']

        REQUEST.RESPONSE.redirect(u+'/manage_main')

def initialize(context):
    context.registerClass(
        QueueCatalog,
        permission='Add ZCatalogs',
        constructors=(manage_addQueueCatalogForm, manage_addQueueCatalog, ),
        icon='www/QueueCatalog.gif',
        )

    context.registerHelp()
    context.registerHelpTitle('Zope Help')
