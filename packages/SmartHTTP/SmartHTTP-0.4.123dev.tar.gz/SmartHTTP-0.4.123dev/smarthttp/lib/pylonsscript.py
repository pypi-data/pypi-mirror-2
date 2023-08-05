#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lib.pylonsscript
    Generic Paste-based script for Pylons.
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
try:
    import subprocess
except ImportError:
    from paste.util import subprocess24 as subprocess
from paste.script.command import Command, BadCommand
from paste.deploy import loadapp, loadserver
import threading
import atexit
import logging
import sys
import re
import os

class PylonsScript(Command):
    usage = 'CONFIG_FILE'
    summary = "Pylons script"
    description = """\
    This class provides support for scripts with db/logging routines from pylons app
    """
    min_args = 0
    takes_config_file = 1
    requires_config_file = True
    default_verbosity = 1
    parser = Command.standard_parser(quiet=True)
    parser.add_option('-d', '--debug',
                      dest='debug',
                      action='store_true',
                      metavar='DEBUG',
                      default=False,
                      help="Enable debug output.")
    parser.add_option('-n', '--app-name',
                      dest='app_name',
                      metavar='NAME',
                      help="Load the named application (default main)")

    parser.add_option('--log-file',
                      dest='log_file',
                      metavar='LOG_FILE',
                      help="Save output to the given log file (redirects stdout)")

   
    possible_subcommands = ()
    _scheme_re = re.compile(r'^[a-z][a-z]+:', re.I)
    
    def __init__(self):
        Command.__init__(self, 'PylonsScript')
    
    def command(self):
        if self.requires_config_file:
            if not self.args:
                raise BadCommand('You must give a config file')
            app_spec = self.args[0]
            if (len(self.args) > 1
                and self.args[1] in self.possible_subcommands):
                cmd = self.args[1]
                restvars = self.args[2:]
            else:
                cmd = None
                restvars = self.args[1:]
        else:
            app_spec = ""
            if (self.args
                and self.args[0] in self.possible_subcommands):
                cmd = self.args[0]
                restvars = self.args[1:]
            else:
                cmd = None
                restvars = self.args[:]

        app_name = self.options.app_name
        vars = self.parse_vars(restvars)
        if not self._scheme_re.search(app_spec):
            app_spec = 'config:' + app_spec
            
        base = os.getcwd()

        if self.options.log_file:
            try:
                writeable_log_file = open(self.options.log_file, 'a')
            except IOError, ioe:
                msg = 'Error: Unable to write to log file: %s' % ioe
                raise BadCommand(msg)
            writeable_log_file.close()

        log_fn = app_spec
        if log_fn.startswith('config:'):
            log_fn = app_spec[len('config:'):]
        elif log_fn.startswith('egg:'):
            log_fn = None
        if log_fn:
            log_fn = os.path.join(base, log_fn)
            self.logging_file_config(log_fn)

        self.log = logging.getLogger(__name__)
        
        app = loadapp(app_spec, name=app_name,
                           relative_to=base, global_conf=vars)

        try:
            self.main()
        except (SystemExit, KeyboardInterrupt), e:
            if self.verbose > 1:
                raise
            if str(e):
                msg = ' '+str(e)
            else:
                msg = ''
            print 'Exiting%s (-v to see traceback)' % msg

    def main(self):
        self.log.info("This is stub method, you should implement it for subclass")

    @classmethod
    def run_script(cls, args=None):
        command = cls()
        if args is None:
            args = sys.argv[1:]
        exit_code = command.run(args)
        

if __name__ == "__main__":
    PylonsScript.run_script()
