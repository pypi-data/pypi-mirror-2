# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lib.maps
    Custom Routes implementation.
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
>>> from smarthttp.sites.arbitrary import ArbitrarySite
>>> ArbitrarySite.map = SmartMap([('page1', '/index.php', {}), ('page2', '/{var1}', {})])
>>> site = ArbitrarySite(domain='test.com')
>>> site.url('page1', fgs='fds')
'http://test.com/index.php?fgs=fds'
>>> site.url('page1')
'http://test.com/index.php'
>>> site.url('page2', var1='test')
'http://test.com/test'
"""
import re
import sys
import urllib
import types
from routes.mapper import Mapper
from routes.route import Route
from routes.util import URLGenerator
from routes.util import _url_quote as url_quote, _str_encode
from smarthttp.lib.containers import SmartDict
import logging
log = logging.getLogger(__name__)

class SmartMap(Mapper):
    """
    Extended Mapper class for SmartHTTP site classes.
    """
    urlgen = None
    def __init__(self, paths=None):
        Mapper.__init__(self)
        self.explicit = True
        if paths:
            for path in paths:
                self.connect(path[0], path[1], **path[2])
        for route in self.matchlist:
            route.hardcoded = []
            route.maxkeys = route.minkeys
            route.generate = types.MethodType(route_generate, route, Route)
        self.urlgen = URLGenerator(mapper=self, environ={'HTTP_HOST':''})

class LocalMap(object):
    """
    This is binding between map for engine and particular site instance, so it correctly understands base_path and domain
    """
    _map = None
    site = None
    urlgen = None
    def __init__(self, site, _map=None):
        self.site = site
        if not _map:
            _map = site.__class__.map
        self._map = _map
        self.urlgen = URLGenerator(mapper=self._map, environ={'SERVER_NAME':site.domain, 'SERVER_PORT':str(site.port)})
        
    def url(self, url, params=None, **kw):
        if url in self._map._routenames:
            route = self._map._routenames[url]
            params = SmartDict(route.defaults.copy()) + params + kw
            params._clean_false()
            route_url = route.generate(**params._dict)
            return self.urlgen(route_url, qualified=True)
        else:
            raise Exception('Unknown url: {0}'.format(url))
        

def route_generate(self, _ignore_req_list=False, _append_slash=False, **kargs):
    """
    Horrible hack in order to make Routes not chew away controller/action vars
    """
    # Verify that our args pass any regexp requirements
    if not _ignore_req_list:
        for key in self.reqs.keys():
            val = kargs.get(key)
            if val and not self.req_regs[key].match(self.make_unicode(val)):
                log.info(key)
                return False

    # Verify that if we have a method arg, its in the method accept list. 
    # Also, method will be changed to _method for route generation
    meth = kargs.get('method')
    if meth:
        if self.conditions and 'method' in self.conditions \
            and meth.upper() not in self.conditions['method']:
            return False
        kargs.pop('method')

    if self.minimization:
        url = self.generate_minimized(kargs)
    else:
        url = self.generate_non_minimized(kargs)
    if url is False:
        return url

    if not url.startswith('/') and not self.static:
        url = '/' + url
    extras = frozenset(kargs.keys()) - self.maxkeys
    if extras:
        if _append_slash and not url.endswith('/'):
            url += '/'
        fragments = []
        # don't assume the 'extras' set preserves order: iterate
        # through the ordered kargs instead
        for key in kargs:
            if key not in extras:
                continue
            val = kargs[key]
            if isinstance(val, (tuple, list)):
                for value in val:
                    fragments.append((key, _str_encode(value, self.encoding)))
            else:
                fragments.append((key, _str_encode(val, self.encoding)))
        if fragments:
            url += '?'
            url += urllib.urlencode(fragments)
        return url
    elif _append_slash and not url.endswith('/'):
        url += '/'
        return url
    return url
