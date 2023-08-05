### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################


# import standard packages
from cStringIO import StringIO
import thread
import time
import traceback

# import local packages
import threadframe


def threads(connection):
    """Dump current threads execution stack
    """
    frames = threadframe.dict()
    this_thread_id = thread.get_ident()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    res = ["Threads traceback dump at %s\n" % now]
    for thread_id, frame in frames.iteritems():
        if thread_id == this_thread_id:
            continue
        # Find request in frame
        reqinfo = ''
        f = frame
        while f is not None:
            request = f.f_locals.get('request')
            if request is not None:
                reqinfo = (request.get('REQUEST_METHOD', '') + ' ' + request.get('PATH_INFO', ''))
                qs = request.get('QUERY_STRING')
                if qs:
                    reqinfo += '?' + qs
                break
            f = f.f_back
        if reqinfo:
            reqinfo = " (%s)" % reqinfo
        output = StringIO()
        traceback.print_stack(frame, file=output)
        res.append("Thread %s%s:\n%s" % (thread_id, str(reqinfo), output.getvalue()))
    frames = None
    res.append("End of dump")
    print >> connection, '\n'.join(res)
