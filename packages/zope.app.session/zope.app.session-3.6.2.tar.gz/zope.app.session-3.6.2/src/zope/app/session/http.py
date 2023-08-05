##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Session implementation using cookies

$Id: http.py 116073 2010-09-01 10:39:46Z menesis $
"""

# BBB
from zope.session.http import (ICookieClientIdManager,
                               MissingClientIdException,
                               notifyVirtualHostChanged,
                               CookieClientIdManager,
                               digestEncode,
                               cookieSafeTrans)
