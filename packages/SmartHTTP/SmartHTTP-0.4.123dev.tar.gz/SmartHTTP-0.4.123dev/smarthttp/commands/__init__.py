# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.commands
    Command-line tools for SmartHTTP
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

from paste.script.command import Command, BadCommand
import os, sys
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
    
    parser.add_option('--url',
                      dest='url',
                      help="Load this url")
    parser.add_option('--baseurl',
                      dest='baseurl',
                      help="Init site with this url.")
    
    parser.add_option('--site',
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
        if not self.options.baseurl and self.options.url:
            self.options.baseurl = self.options.url
        if self.options.site:
            pkg, cls = self.options.site.rsplit('.', 1)
            print pkg
            print cls
            exec ('from {0} import *'.format(pkg)) in locs
            Site = locs[cls]
        else:
            from smarthttp.sites.arbitrary import ArbitrarySite
            Site = ArbitrarySite
            exec ('from smarthttp.sites.arbitrary import *') in locs
        locs['Site']       = Site
        locs['site']       = Site(client=locs['client'], url=self.options.baseurl)
        exec ('from smarthttp.html import *') in locs
        if self.options.url:
            locs['req']    = locs['site'].request(self.options.url)
            locs['url']    = self.options.url
        else:
            locs['req']    = None
            locs['url']    = None
            
        banner = """SmartHTTP interactive shell.\n"""\
                 """\tclient = HTTPClient()\n"""\
                 """\tsite   = {0[site]}\n"""\
                 """\turl    = {0[url]}\n"""\
                 """\treq    = {0[req]}\n""".format(locs)

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

