# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.client
    HTTP client abstraction layer
    Last changed on Wed Apr 14 14:50:37 2010 +1100 rev. 111:5efdacc70dde by Dan Kluev <orion@ssorion.info>

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
"""

import os, random
import logging
from smarthttp.envspec.http import DoHTTPRequest
log = logging.getLogger(__name__)

user_agents = open(os.path.join(os.path.dirname(__file__), 'ua.txt')).read().split('\n')

class HTTPClient(object):
    def __init__(self, thread=None, logger=None, ua=None):
        global log
        self.thread = thread
        if logger:
            self.log = logger
        elif self.thread:
            self.log = logging.getLogger("%s.client" % (thread.name))
        else:
            self.log = logging.getLogger(__name__)
        self.cookies = {}
        if ua:
            self.user_agent = ua
        else:
            self.user_agent = random.choice(user_agents)
        self.history = []

    def load(self, site):
        site.load(self)

    def request(self, url, data=None, referer=None, request="GET", retry=5, timeout=120):
        if not referer:
            if self.history:
                referer = self.history[-1]['url']
            else:
                referer = url
        attempt = 1
        while attempt < retry:
            if self.thread:
                self.thread.check_kill()
            reply = DoHTTPRequest(url, data=data, referer=referer, request=request, cookies=self.cookies, user_agent=self.user_agent, logger=self.log, timeout=timeout)
            if self.thread:
                self.thread.check_kill()
            if reply.error:
                self.log.debug("Attempt %s failed for url %s" % (attempt, url))
                attempt += 1
            else:
                break
        self.cookies = reply.cookies
        self.history.append({'url':url})
        return reply
