# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.commands
    Command-line tools
    Last changed on 2010-07-14 20:28:41+11:00 rev. 271:1656a4be55dd by Dan Kluev <dan@kluev.name>

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


Command-line tools
==================

.. _smarthttp.commands-ShellCommand:

:class:`ShellCommand`
---------------------

Open an interactive shell with SmartHTTP modules initialized.

    The optional CONFIG_FILE argument specifies the config file to use for
    the interactive shell. CONFIG_FILE defaults to 'development.ini'.
    
    Use --url to load particular url, or --site to load particular site module.
    
    Example::
    
            $ paster shell my-development.ini
               
    

.. autoclass:: ShellCommand
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from paste.script.command import Command, BadCommand
import os
import sys
import paste.fixture
import paste.registry
import paste.deploy.config

class ShellCommand(Command):
    """Open an interactive shell with SmartHTTP modules initialized.

    The optional CONFIG_FILE argument specifies the config file to use for
    the interactive shell. CONFIG_FILE defaults to 'development.ini'.
    
    Use --url to load particular url, or --site to load particular site module.
    
    Example::
    
            $ paster shell my-development.ini
               
    """
    summary = __doc__.splitlines()[0]
    usage = '\n' + __doc__

    min_args = 0
    max_args = 1
    group_name = 'smarthttp'
    parser = Command.standard_parser(simulate=True)
    parser.add_option('-d', '--disable-ipython',
                      action='store_true',
                      dest='disable_ipython',
                      help="Don't use IPython if it is available")
    parser.add_option('-m', '--manager',
                      action='store_true',
                      dest='manager',
                      default=False,
                      help='Load site-handler manager',
                      )
    
    parser.add_option('-u', '--url',
                      dest='url',
                      help="Load this url")
    parser.add_option('-b', '--baseurl',
                      dest='baseurl',
                      help="Init site with this url.")
    
    parser.add_option('-s', '--site',
                      dest='site',
                      help='Use this site instead of ArbitrarySite')
    
    def command(self):
        """Main command to create a new shell"""
        self.verbose = 3
        if len(self.args) == 0:
            # Assume the .ini file is ./development.ini
            config_file = 'development.ini'
            if not os.path.isfile(config_file):
                raise BadCommand('%sError: CONFIG_FILE not found at: .%s%s\n'
                                 'Please specify a CONFIG_FILE' % \
                                 (self.parser.get_usage(), os.path.sep,
                                  config_file))
        else:
            config_file = self.args[0]

        config_name = 'config:%s' % config_file
        here_dir = os.getcwd()
        if not self.options.quiet:
            # Configure logging from the config file
            self.logging_file_config(config_file)
        sys.path.insert(0, here_dir)
        
        locs = {'__name__':'shell'}
        from smarthttp.client import HTTPClient
        locs['HTTPClient'] = HTTPClient
        locs['client']     = HTTPClient()
        if self.options.manager:
            from smarthttp.sites.manager import SiteManager
            locs['manager'] = manager = SiteManager(lib=True)
        if not self.options.baseurl and self.options.url:
            self.options.baseurl = self.options.url
        Site = None
        if self.options.site:
            if self.options.manager:
                Site = manager.get_handler(name=self.options.site)
            if not Site and '.' in self.options.site:
                pkg, cls = self.options.site.rsplit('.', 1)
                exec ('from {0} import *'.format(pkg)) in locs
                Site = locs[cls]
            if not Site:
                print "Could not find handler '{0}'".format(self.options.site)
        if not Site and self.options.manager and self.options.url:
            Site = manager.get_handler(url=self.options.url)
        if not Site:
            from smarthttp.sites.arbitrary import ArbitrarySite
            Site = ArbitrarySite
            exec ('from smarthttp.sites.arbitrary import *') in locs
        locs['Site']       = Site
        locs['site']       = Site(client=locs['client'], url=self.options.baseurl)
        exec ('from smarthttp.html import *') in locs
        if self.options.url:
            locs['url']    = locs['site'].url(self.options.url)
            locs['req']    = locs['site'].request(locs['url'])
            locs['doc']    = locs['req'].autoparse()
        else:
            locs['req']    = None
            locs['url']    = None
            locs['doc']    = None
            
        banner = """SmartHTTP interactive shell.\n"""\
                 """\tclient = HTTPClient()\n"""\
                 """\tsite   = {0[site]}\n"""\
                 """\turl    = {0[url]}\n"""\
                 """\treq    = {0[req]}\n"""\
                 """\tdoc    = {0[doc]}\n""".format(locs)

        try:
            if self.options.disable_ipython:
                raise ImportError()

            # try to use IPython if possible
            from IPython.Shell import IPShellEmbed

            shell = IPShellEmbed(argv=self.args)
            shell.set_banner(shell.IP.BANNER + '\n\n' + banner)
            try:
                shell(local_ns=locs, global_ns={})
            finally:
                paste.registry.restorer.restoration_end()
        except ImportError:
            import code
            py_prefix = sys.platform.startswith('java') and 'J' or 'P'
            newbanner = "Pylons Interactive Shell\n%sython %s\n\n" % \
                (py_prefix, sys.version)
            banner = newbanner + banner
            shell = code.InteractiveConsole(locals=locs)
            try:
                import readline
            except ImportError:
                pass
            try:
                shell.interact(banner)
            finally:
                paste.registry.restorer.restoration_end()

