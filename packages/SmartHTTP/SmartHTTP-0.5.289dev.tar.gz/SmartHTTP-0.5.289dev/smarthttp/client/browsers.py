# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.client.browsers
    Browser imitation
    Last changed on 2010-05-16 01:17:36+11:00 rev. 179:97351786f3d8 by Dan Kluev <orion@ssorion.info>

..
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Browser imitation
=================


"""
__docformat__ = 'restructuredtext'
from smarthttp import __version__
from smarthttp.envspec.http import DoHTTPRequest, library_version
import random

class Browser:
    platform = None
    user_agent = None
    version = None
    versions = None
    locale = 'en-US'
    def __init__(self, platform=None):
        self.platform = platform
        if self.versions and not self.version:
            self.version = random.choice(self.versions)

class Firefox(Browser):
    def __init__(self, platform=None):
        Browser.__init__(self, platform)
        self.version  = '3.6.3'
        self.revision = '1.9.2.3'
        self.gecko    = '20100416'
        self.user_agent = "Mozilla/5.0 ({0.platform_string} {0.locale}; rv:{0.revision}) Gecko/{0.gecko} Firefox/{0.version}".format(self)
        
    @property
    def platform_string(self):
        return "{0.ui}; U; {0.version_str};".format(self.platform)

class MSIE(Browser):
    versions = ['5.0', '5.5', '6.0', '7.0', '8.0']
    def __init__(self, platform=None):
        Browser.__init__(self, platform)
        self.user_agent = "Mozilla/4.0 (compatible; MSIE {0.version}; {1.version_str})".format(self, self.platform)

class Safari(Browser):
    """
    Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Safari/530.17
    """
    def __init__(self, platform=None):
        Browser.__init__(self, platform)
        self.user_agent = "Mozilla/5.0 ({1.ui}; U; {1.version_str}; {0.locale}) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Safari/530.17".format(self, self.platform)

class Opera(Browser):
    """
    Opera/9.52 (X11; Linux x86_64; U; en)
    Opera/9.80 (Windows NT 6.0; U; en) Presto/2.2.15 Version/10.00
    Opera/9.80 (X11; Linux i686; U; en) Presto/2.2.15 Version/10.00
    Opera/10.00 (Windows NT 5.1; U; ru) Presto/2.2.0
    """
    def __init__(self, platform=None):
        Browser.__init__(self, platform)
        self.user_agent = "Opera/9.80 ({1.version_str}; U; {0.locale}) Presto/2.2.15 Version/10.00".format(self, self.platform)

class Chrome(Browser):
    """
    Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.307.5 Safari/532.9
    """
    def __init__(self, platform=None):
        Browser.__init__(self, platform)
        self.user_agent = "Mozilla/5.0 ({1.ui}; U; {1.version_str}; {0.locale}) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.307.5 Safari/532.9".format(self, self.platform)

class SmartHTTP(Browser):
    def __init__(self, platform=None):
        Browser.__init__(self, platform)
        self.version = __version__
        self.library = library_version
        self.user_agent = "SmartHTTP/{0.version} ({0.library}; {1.version_str})".format(self, self.platform)

all_browsers = [Firefox, MSIE, Safari, Opera, Chrome]
