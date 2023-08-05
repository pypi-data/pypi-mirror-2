# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.decorators
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
"""
__docformat__ = 'restructuredtext'

from decorator import decorator

from .exceptions import ParseException, ResultException, SmartHTTPException
from .http import HTTPResponse

import logging
log = logging.getLogger(__name__)

class ParserDecorator(object):
    """Class for parser decorators.
    """
    smap = None
    def __init__(self, smap):
        self.smap = smap
        self.parser_decorator = decorator(self.parser)

    def map_route(self, route):
        def do_mapping(func, *args, **kw):
            mapped_func = self.parser_decorator(func)
            #log.info("do_mapping({0}, {1}, {2}, {3}, {4})".format(route, func, mapped_func, args, kw))
            self.smap.map_parser(route, mapped_func)
            return mapped_func
        return do_mapping

    def parser(self, func, func_self, resp, *args, **kw):
        """
        This decorator will catch parsing exceptions and gracefully return site.error()
        """
        if not isinstance(resp, HTTPResponse):
            return func_self.error(u"resp is of type {0} instead of HTTPResponse".format(type(resp)), resp=resp)
        try:
            res = func(func_self, resp, *args, **kw)
            if not res or not hasattr(res, 'data'):
                raise ParseException(u"Function {0} returned invalid value {1}".format(func, res))
            res.resp = resp
            return res
        except ParseException, e:
            return func_self.error(str(e), resp=resp)
    
    def __call__(self, route=None, *args, **kw):
        """Decorate parsing function. Can be called in @parser or @parser(route) forms
        """
        is_callable = hasattr(route, '__call__')
        if is_callable:
            return self.parser_decorator(route)
        else:
            return self.map_route(route)


