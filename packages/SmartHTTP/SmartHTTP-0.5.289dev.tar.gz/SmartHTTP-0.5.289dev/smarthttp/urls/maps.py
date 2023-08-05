# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.urls.maps
    Custom Routes
    Last changed on 2010-07-14 21:31:40+11:00 rev. 275:905c3d367794 by Dan Kluev <dan@kluev.name>

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


Custom Routes
=============

.. note::

    Based on Routes package, released by Ben Bangert <ben@groovie.org>
    See http://routes.groovie.org/index.html for details
    
>>> from smarthttp.sites.arbitrary import ArbitrarySite
>>> ArbitrarySite.map = SmartMap([('page1', '/index.php', {}), ('page2', '/{var1}', {})])
>>> site = ArbitrarySite(domain='test.com')
>>> site.url('page1', fgs='fds')
<URL(http://test.com/index.php?fgs=fds)>
>>> site.url('page1')
<URL(http://test.com/index.php)>
>>> site.url('page2', var1='test')
<URL(http://test.com/test)>
>>> site = ArbitrarySite(url='http://test.com/?asdf=/')
>>> site.map.urlgen('/test', qualified=True)
'http://test.com/?asdf=/test'

.. todo::
   * Needs far more extensive testing.
   * Relation with Routes should be better designed

.. _smarthttp.urls.maps-LocalMap:

:class:`LocalMap`
-----------------


    This is binding between map for engine and particular site instance, so it correctly understands base_path and domain
    

.. autoclass:: LocalMap
    :members:
    :undoc-members:

.. _smarthttp.urls.maps-SmartRoute:

:class:`SmartRoute`
-------------------



.. autoclass:: SmartRoute
    :members:
    :undoc-members:

.. _smarthttp.urls.maps-SmartMap:

:class:`SmartMap`
-----------------


    Extended Mapper class for SmartHTTP site classes.
    

.. autoclass:: SmartMap
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

import re
import sys
import types
from routes.mapper import Mapper
from routes.route import Route
from routes.util import URLGenerator
from routes.util import _url_quote as url_quote, _str_encode
from ..lib.containers import SmartDict
from ..exceptions import SmartHTTPException
from ..decorators import ParserDecorator
from . import URL, urlencode
import logging
log = logging.getLogger(__name__)

class SmartMap(Mapper):
    """
    Extended Mapper class for SmartHTTP site classes.
    """
    urlgen = None
    parsers = None
    routes  = None
    def __init__(self, paths=None):
        """Create mapper with according routes.

        .. todo:: Add all needed features for routes, including optionality, aliases, conversions, etc
        """
        Mapper.__init__(self)
        self.routes = self._routenames
        self.explicit = True
        if paths:
            for path in paths:
                self.connect(path[0], path[1], **path[2])
        for route in self.matchlist:
            route.hardcoded = []
            route.maxkeys = route.minkeys
        self.urlgen = URLGenerator(mapper=self, environ={'HTTP_HOST':''})
        self.parser = ParserDecorator(self)
        self.parsers = {}

    def map_parser(self, routes, func):
        """Maps route and parsing function.
        """
        if not isinstance(routes, list) and not isinstance(routes, set):
            routes = [routes]
        self.parsers[func] = routes
        for route in routes:
            if route in self.routes:
                self.routes[route].parsers.append(func)

    # From Routes package

    def connect(self, *args, **kargs):
        """Create and connect a new Route to the Mapper.
        
        Usage:
        
        .. code-block:: python
        
            m = Mapper()
            m.connect(':controller/:action/:id')
            m.connect('date/:year/:month/:day', controller="blog", action="view")
            m.connect('archives/:page', controller="blog", action="by_page",
            requirements = { 'page':'\d{1,2}' })
            m.connect('category_list', 'archives/category/:section', controller='blog', action='category',
            section='home', type='list')
            m.connect('home', '', controller='blog', action='view', section='home')

        .. todo:: move route-specific code from __init__ to here, add w/e specific code package needs.
        
        """
        routename = None
        if len(args) > 1:
            routename = args[0]
        else:
            args = (None,) + args
        if '_explicit' not in kargs:
            kargs['_explicit'] = self.explicit
        if '_minimize' not in kargs:
            kargs['_minimize'] = self.minimization
        route = SmartRoute(*args, **kargs)
                
        # Apply encoding and errors if its not the defaults and the route 
        # didn't have one passed in.
        if (self.encoding != 'utf-8' or self.decode_errors != 'ignore') and \
           '_encoding' not in kargs:
            route.encoding = self.encoding
            route.decode_errors = self.decode_errors
        
        if not route.static:
            self.matchlist.append(route)
        
        if routename:
            self._routenames[routename] = route
            route.name = routename
        if route.static:
            return
        exists = False
        for key in self.maxkeys:
            if key == route.maxkeys:
                self.maxkeys[key].append(route)
                exists = True
                break
        if not exists:
            self.maxkeys[route.maxkeys] = [route]
        self._created_gens = False


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
        self.urlgen = URLGenerator(mapper=self._map, environ={'SERVER_NAME':site.domain, 'SERVER_PORT':str(site.port), 'SCRIPT_NAME':site.base_path})
        
    def url(self, url, params=None, **kw):
        if url in self._map._routenames:
            route = self._map._routenames[url]
            params = SmartDict(route.defaults.copy()) + params + kw
            params._clean_false()
            route_url = route.generate(**params)
            if not route_url:
                raise SmartHTTPException('Route url generation failed! Route: {0}, params: {1}'.format(url, params))
            return self.urlgen(route_url, qualified=True)
        else:
            raise SmartHTTPException('Unknown url: {0}'.format(url))

    def get_parsers(self, route):
        """Find all parsers for route
        """
        if route in self._map.routes:
            return self._map.routes[route].parsers
        else:
            return []
        
class SmartRoute(Route):
    parsers = None
    def __init__(self, _routename, _routepath, **kargs):
        """Initialize a route, with a given routepath for
        matching/generation
        
        The set of keyword args will be used as defaults.
        
        Usage::
        
            >>> newroute = SmartRoute(None, ':controller/:action/:id')
            >>> sorted(newroute.defaults.items())
            [('action', 'index'), ('id', None)]
            >>> newroute = SmartRoute(None, 'date/:year/:month/:day',  
            ...     controller="blog", action="view")
            >>> newroute = SmartRoute(None, 'archives/:page', controller="blog", 
            ...     action="by_page", requirements = { 'page':'\d{1,2}' })
            >>> newroute.reqs
            {'page': '\\\d{1,2}'}
        
        .. Note:: 
            Route is generally not called directly, a Mapper instance
            connect method should be used to add routes.
        
        """
        self.routepath = _routepath
        self.sub_domains = False
        self.prior = None
        self.parsers = []
        self.redirect = False
        self.name = _routename
        self._kargs = kargs
        self.minimization = kargs.pop('_minimize', False)
        self.encoding = kargs.pop('_encoding', 'utf-8')
        self.reqs = kargs.get('requirements', {})
        self.decode_errors = 'replace'
        
        # Don't bother forming stuff we don't need if its a static route
        self.static = kargs.pop('_static', False)
        self.filter = kargs.pop('_filter', None)
        self.absolute = kargs.pop('_absolute', False)
        
        # Pull out the member/collection name if present, this applies only to
        # map.resource
        self.member_name = kargs.pop('_member_name', None)
        self.collection_name = kargs.pop('_collection_name', None)
        self.parent_resource = kargs.pop('_parent_resource', None)
        
        # Pull out route conditions
        self.conditions = kargs.pop('conditions', None)
        
        # Determine if explicit behavior should be used
        self.explicit = kargs.pop('_explicit', False)
                
        # Since static need to be generated exactly, treat them as
        # non-minimized
        if self.static:
            self.external = '://' in self.routepath
            self.minimization = False
        
        # Strip preceding '/' if present, and not minimizing
        if _routepath.startswith('/') and self.minimization:
            self.routepath = _routepath[1:]
        self._setup_route()

    def generate(self, _ignore_req_list=False, _append_slash=False, **kargs):
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
                url += urlencode(fragments)
            return url
        elif _append_slash and not url.endswith('/'):
            url += '/'
            return url
        return url
