# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.manager
    Site handlers Manager
    Last changed on 2010-07-13 18:01:13+11:00 rev. 268:a3501300d9b0 by Dan Kluev <dan@kluev.name>

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


Site handlers Manager
=====================

.. _smarthttp.sites.manager-SiteManager:

:class:`SiteManager`
--------------------


    Holds site-handlers and domains map
    

.. autoclass:: SiteManager
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

import imp
import os
import sys
from ..urls import URL
from . import SiteHandler, SpecificSite, SiteEngine
import logging
log = logging.getLogger(__name__)

class SiteManager(object):
    """
    Holds site-handlers and domains map
    """
    handlers = None
    class_names = None
    domains  = None
    lib      = False
    paths    = None
    def __init__(self, lib=True, paths=None):
        """
        Loads classes.
        :param lib: specifies whether it should load site-handlers provided by library itself
        :param paths: list of tuples (path, module) for recursive look-up to load app-specific handlers
        """
        self.handlers = []
        self.class_names = {}
        self.domains = {}
        self.lib = lib
        self.paths = paths or []
        
        if lib:
            self.load_lib_sites()

    def get_handler(self, name=None, domain=None, url=None, req=None):
        """
        Look up handler by specified parameters.
        Parameter priorities are:
        name, domain, url, request
        :param url: :class:`~smarthttp.urls.URL` or string, includes domain look-up
        :param req: :class:`~smarthttp.http.HTTPResponse`, includes url and domain look-up
        :rtype: :class:`~smarthttp.sites.SiteHandler` subclass or `None`
        """
        if name:
            if name in self.class_names:
                return self.class_names[name]

        if not url and req:
            url = req.url
        
        if url and not isinstance(url, URL):
            url = URL(url)

        if not domain and url:
            domain = url.hostname

        if domain:
            # Should recursively drop subdomains actually
            if domain in self.domains:
                return self.domains[domain]
            
        return None
            
    def load_lib_sites(self):
        sitedir = os.path.dirname(os.path.abspath(__file__))
        libdir  = os.path.dirname(os.path.dirname(sitedir))
        for fn in os.listdir(sitedir):
            fullpath = os.path.join(sitedir, fn)
            if os.path.isdir(fullpath) and os.path.isfile(os.path.join(fullpath, '__init__.py')):
                modname = u"smarthttp.sites.{0}".format(fn)
                self.recursive_import(fullpath, modname, libdir)

    def import_handlers(self, module_name, pkgpath):
        module_desc = imp.find_module(module_name.replace('.', os.path.sep), [pkgpath])
        module = None
        if module_desc:
            try:
                module = imp.load_module(module_name, *module_desc)
            finally:
                if module_desc[0]:
                    module_desc[0].close()
        if module:
            class_list = filter(lambda x: x.__class__ == type and issubclass(x, SiteHandler) and not x in [SiteHandler, SpecificSite, SiteEngine],\
                                module.__dict__.values())
            for cls in class_list:
                if not cls in self.handlers:
                    self.handlers.append(cls)
                    self.class_names[cls.__name__] = cls
                    if cls.domain:
                        self.domains[cls.domain] = cls
    
    def recursive_import(self, path, package, pkgpath):
        if os.path.isfile(os.path.join(path, '__init__.py')):
            self.import_handlers(package, pkgpath)
        for filename in os.listdir(path):
            fp = os.path.join(path, filename)
            if os.path.isdir(fp):
                self.recursive_import(fp, u"{0}.{1}".format(package, filename), pkgpath)
            else:
                if filename.endswith('.py'):
                    mn = filename.split('.')[0]
                    if mn != "__init__":
                        mp = u"{0}.{1}".format(package, mn)
                        try:
                            self.import_handlers(mp, pkgpath)
                        except Exception, e:
                            log.error("Import {0} from {2} failed due {3}".format(mp, fp, pkgpath, e))

    def __repr__(self):
        return "<SiteManager(lib={0.lib}, {1} external paths, {2} handlers>".format(self, len(self.paths), len(self.handlers))

