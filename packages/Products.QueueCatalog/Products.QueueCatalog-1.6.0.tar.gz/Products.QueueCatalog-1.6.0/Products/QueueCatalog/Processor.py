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
"""
$Id: Processor.py 86692 2008-05-13 10:38:28Z andreasjung $
"""

import thread
import Zope
from time import sleep
import sys
from zLOG import LOG, ERROR, PANIC, INFO

class Processor:
    """Simple thread that processes queued catalog events
    """

    def __init__(self, queue_catalog_paths, interval=60):
        self._queue_catalog_paths = queue_catalog_paths
        self._interval = interval
        thread.start_new_thread(self.live, ())

    def live(self):
        LOG('QueuedCatalog', INFO, 'Set up to process queue entries')
        while 1:
            sleep(self._interval)
            for queue_catalog_path in self._queue_catalog_paths:
                try:
                    application = Zope.app()
                except:
                    LOG('QueuedCatalog', PANIC,
                        "Couldn't connect to database",
                        error=sys.exc_info())
                    break # No point in doing any more paths right now
                else:

                    try:
                        queue_catalog = application.unrestrictedTraverse(
                            queue_catalog_path)
                        queue_catalog.process()
                    except:
                        LOG('QueuedCatalog', ERROR, 'Queue processing failed',
                            error=sys.exc_info())

                    else:
                        LOG('QueuedCatalog', INFO, 'Processed queue')
                    
                    application._p_jar.close()

__doc__ = Processor.__doc__ + __doc__

