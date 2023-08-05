#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
openvas.oaplib.cmd - An OAP (OpenVAS Administration Protocol) command line client.
"""
#
# Copyright 2010 by Hartmut Goebel <h.goebel@goebel-consult.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Hartmut Goebel <h.goebel@goebel-consult.de>"
__copyright__ = "Copyright 2010 by Hartmut Goebel <h.goebel@goebel-consult.de>"
__licence__ = "GNU General Public License version 3 (GPL v3)"
__version__ = '0.0.1'

from openvas.oaplib import *
# use the same etree implementations as oaplib
from openvas.oaplib import etree

import inspect
import sys
import time
import argparse
import textwrap
import getpass

try:
    from gettext import gettext
except ImportError:
    def gettext(message):
        return message
_ = gettext


class OAPCommandClient(object):
    def __init__(self, args):
        self.client = OAPClient(args.host, args.port,
                                args.username, args.password)

    def run_command(self, optparser, args):
        mod = inspect.getmodule(self)
        cmd = getattr(mod, args.command_name.replace('-', '_'))
        self.client.open()
        try:
            res = cmd.run(self.client, args)
        except Error, e:
            sys.exit('Error: %s' % e)
        finally:
            self.client.close()
        return res
        
    @classmethod
    def _find_commands(klass):
        def is_OAPCommand(c):
            return inspect.isclass(c) and OAPCommand in c.__bases__
        
        classes = inspect.getmembers(inspect.getmodule(klass), is_OAPCommand)
        return (c[1] for c in classes)


class OAPCommand(object):
    @classmethod
    def _argparse(klass, subparsers):
        cmd_name = klass.__name__.replace('_', '-')
        description = klass.__doc__
        help = description.lstrip().split('\n', 1)[0]
        description = textwrap.dedent(description)
        sp = subparsers.add_parser(cmd_name,
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   help=help,
                                   description=description)
        klass._add_arguments(sp)

#--- basic commands ---

class help(OAPCommand):
    """
    Get help message from OAP server
    """
    
    @staticmethod
    def _add_arguments(sp): pass

    @staticmethod
    def run(oap_client, args):
        res = oap_client.help()
        print res.strip('\n')


class xml(OAPCommand):
    """
    Send plain XML command
    """
    
    @staticmethod
    def _add_arguments(sp):
        sp.add_argument('xml', nargs=1, help='XML text/document to send')

    @staticmethod
    def run(oap_client, args):
        res = oap_client.xml(args.xml[0], xml_result=True)
        print etree.tostring(res)


class get_version(OAPCommand):
    """
    Get the OAP versions supported by the administrator.

    Versions are separated by spaces. The first version is the one the
    administrator prefers.
    """
    
    @staticmethod
    def _add_arguments(sp): pass

    @staticmethod
    def run(oap_client, args):
        pref, versions = oap_client.get_version()
        print pref, ' '.join(versions)


#--- user management ---

class create_user(OAPCommand):
    """
    Create a new user
    """
    
    @staticmethod
    def _add_arguments(sp):
        sp.add_argument('name', help="Name for the new user")
        sp.add_argument('--new_password', required=True,
                        help="Password for new user ('-' to be prompted)")
        sp.add_argument('--role', help="Role user", choices=ROLES)

    @staticmethod
    def run(oap_client, args):
        password = args.new_password
        if password == '-':
            password = getpass.getpass('Password for new OpenVAS user: ')
        # todo: read hosts from stdin
        hosts = ""
        oap_client.create_user(name=args.name, password=password,
                               role=args.role, hosts=hosts)

class get_users(OAPCommand):
    """
    Get details about one or all users
    """
    
    @staticmethod
    def _add_arguments(sp):
        sp.add_argument('name', nargs='*',
                        help='Name of user about which to retrieve details')

    @staticmethod
    def run(oap_client, args):
        def print_user(user):
            print "%(name)-10s\t%(role)-14s\t" % user,
            # todo: complete this depending on allow/denny state
            if user['hosts'] is not None:
                print user['hosts'].replace('\n',' ')
            else:
                print

        if args.name:
            for name in args.name:
                print_user(oap_client.get_users(name))
        else:
            for user in oap_client.get_users():
                print_user(user)


class modify_user(OAPCommand):
    """
    Modfiy an existing user
    """
    
    @staticmethod
    def _add_arguments(sp):
        sp.add_argument('name', help="Name for the new user")
        sp.add_argument('--new-password',
                        help="Password for new user ('-' to be prompted)")
        sp.add_argument('--role', help="Role user", choices=ROLES)

    @staticmethod
    def run(oap_client, args):
        password = args.new_password
        if password == '-':
            password = getpass.getpass('Password for new OpenVAS user: ')
        # todo: read hosts from stdin
        hosts = ""
        oap_client.modify_user(name=args.name, password=password,
                               role=args.role, hosts=hosts)
    

class delete_user(OAPCommand):
    """
    Delete one or more users
    """
    
    @staticmethod
    def _add_arguments(sp):
        sp.add_argument('name', nargs='+', help="Name of user to delete")

    @staticmethod
    def run(oap_client, args):
        for name in args.name:
            oap_client.delete_user(name)

#--- feeds ---

class describe_feed(OAPCommand):
    """
    Get details about the NVT feed this administrator uses
    """
    
    @staticmethod
    def _add_arguments(sp): pass

    @staticmethod
    def run(oap_client, args):
        res = oap_client.describe_feed()
        print 'Name:\t\t%s' % res['name'].strip()
        if res.has_key('version'):
            print 'Version:\t%s' % res['version'].strip()
        print textwrap.fill(res['description'],
                            initial_indent   ='Description:\t',
                            subsequent_indent='\t\t')
        syncing = res.get('currently_syncing', None)
        if syncing:
            print 'Currently Synchronizing:\t%s\t%s' % (syncing['user'].strip(),
                                        syncing['timestamp'])

class sync_feed(OAPCommand):
    """
    Synchronize with the NVT feed
    """
    
    @staticmethod
    def _add_arguments(sp): pass

    @staticmethod
    def run(oap_client, args):
        oap_client.sync_feed()


#--- misc. ---

class describe_auth(OAPCommand):
    """
    Get details about the used authentication methods
    """
    @staticmethod
    def _add_arguments(sp): pass

    @staticmethod
    def run(oap_client, args):
        print oap_client.describe_auth()


class get_settings(OAPCommand):
    """
    Get settings
    """
    
    @staticmethod
    def _add_arguments(sp): pass
        
    @staticmethod
    def run(oap_client, args):
        settings = oap_client.get_settings()
        first = True
        for setting in settings:
            print ('Setting: %s\t(%seditable)'
                   % (setting['sourcefile'],
                      '' if int(setting['editable']) else 'not '))
            for k, v in sorted(setting['items'].items()):
                print '  %s\t%s' % (k, v)
            if not first:
                print
            first = False


def run():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="help",
                        help=_("show this help message and exit"))
    parser.add_argument("--version", action='version', version=__version__)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Verbose messages.")
    parser.add_argument('-P', '--prompt', action='store_true',
                        help="Prompt to exit.")

    group = parser.add_argument_group('Options for connecting to the administrator')
    group.add_argument('-h', '--host', default=ADMINISTRATOR_ADDRESS,
                       help=("Connect to administrator on host HOST "
                             "(default: %(default)s)"))
    group.add_argument('-p', '--port', type=int, default=ADMINISTRATOR_PORT,
                       help="Use port number PORT (default: %(default)s)")
    group.add_argument('-u', '--username', default=getpass.getuser(),
                       help="OAP username (default: current user's name)")
    group.add_argument('-w', '--password',
                       help="OAP password (default: same as username)")

    subparsers = parser.add_subparsers(dest='command_name',
                                       title='Available OAP commands',
                                       help='Get help for sub-commands with <cmd> --help')

    for cmd in OAPCommandClient._find_commands():
        cmd._argparse(subparsers)

    args = parser.parse_args()
    
    if not (0 < args.port < 65536):
        parser.error('Administrator port must be a number between 1 and 65535.')
    if args.password is None:
        args.password = args.username

    client = OAPCommandClient(args)
    client.run_command(parser, args)

if __name__ == '__main__':
    run()
