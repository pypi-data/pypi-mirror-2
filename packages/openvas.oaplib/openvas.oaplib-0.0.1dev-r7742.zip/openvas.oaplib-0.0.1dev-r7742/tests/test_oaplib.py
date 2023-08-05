# -*- coding: utf-8 -*-
"""
Testsuite for openvas.oaplib
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

import unittest
import os
import inspect
import random
import socket
import sys

import openvas.oaplib
from openvas.oaplib import etree

class OAPTestBase(unittest.TestCase):
    _OAP_HOST = None
    _OAP_PORT = None
    _OAP_USER = None
    _OAP_PASSWD = None

    def setUp(self):
        self.client = openvas.oaplib.OAPClient(self._OAP_HOST, self._OAP_PORT,
                                               self._OAP_USER, self._OAP_PASSWD)
        self.client.open()

    def tearDown(self):
        self.client.close()


class TestOAP(OAPTestBase):

    def test_help(self):
        self.client.help()

    def test_xml_0(self):
        text = self.client.xml('<help/>')
        self.assert_(isinstance(text, basestring))
        self.assert_(text != '')

    def test_xml_1(self):
        xml = self.client.xml('<help/>', xml_result=True)
        self.assert_(etree.iselement(xml))

    def test_get_version(self):
        ver = self.client.get_version()
        self.assert_(isinstance(ver, tuple))
        self.assertEqual(len(ver), 2)
        self.assert_(isinstance(ver[0], basestring))
        self.assert_(isinstance(ver[1], (tuple, list)))

    #--- users ---

    def test_user(self):
        name = "oap_test_user"
        password = ''.join((name, str(id(self))))
        try:
            self.client.create_user(name, password, "User", "allow any")
            users = self.client.get_users()
            self.assert_(inspect.isgenerator(users))
            for user in users:
                self.assert_(isinstance(user, dict))
            user = self.client.get_users(name)
            self.assert_(isinstance(user, dict))
            self.assert_(user['name'] == name)
        finally:
            self.client.delete_user(name)

    def test_modify_user(self):
        name = "oap_test_user"
        password = ''.join((name, str(id(self))))
        try:
            self.client.create_user(name, password, "User", "allow all")
            self.client.modify_user(name, role="Admin")
            user = self.client.get_users(name)
            self.assert_(user['role'] == "Admin")

            self.client.modify_user(name, hosts="deny all")
            user = self.client.get_users(name)
            self.assert_(user['hosts'] == "deny all")

            self.client.modify_user(name, password=password[::-1])
        finally:
            self.client.delete_user(name)

    #----

    def test_describe_feed(self):
        feed = self.client.describe_feed()
        self.assert_(isinstance(feed, dict))
        self.assert_(feed.has_key('name'))
        self.assert_(feed.has_key('description'))

    def test_sync_feed(self):
        feed = self.client.sync_feed()
        self.assert_(feed is None)
        feed = self.client.describe_feed()
        # assume our request is faster than the sync finishes
        self.assert_(feed.has_key('currently_syncing'))

    #----
    
    def test_describe_auth(self):
        try:
            text = self.client.describe_auth()
        except openvas.oaplib.ClientError, e:
            self.assertEqual(e.args,
                             ('describe_auth', '404', 'Resource missing'))
        else:
            self.assert_(isinstance(text, basestring))

    def test_get_settings(self):
        settings = self.client.get_settings()
        self.assert_(isinstance(settings, list))
        for setting in settings:
            self.assert_(setting.has_key('sourcefile'))
            self.assert_(setting.has_key('editable'))
            self.assert_(setting.has_key('items'))
            self.assert_(isinstance(setting['items'], dict))


class main(unittest.main):
    def parseArgs(self, argv):
        """

Examples:
  %prog                            - run default set of tests
  %prog MyTestSuite                - run suite 'MyTestSuite'
  %prog MyTestCase.testSomething   - run MyTestCase.testSomething
  %prog MyTestCase                 - run all 'test*' test methods
                                               in MyTestCase
        """
        import getpass
        import optparse
        parser = optparse.OptionParser('usage: %prog [options] [test] [...]' +
                                       self.parseArgs.__doc__.rstrip(),
                                       add_help_option=False)
        parser.add_option("--help", action="help",
                          help="show this help message and exit")
        parser.set_defaults(verbosity=1)
        parser.add_option('-v', '--verbose', dest='verbosity',
                          action='store_const', const=2)
        parser.add_option('-q', '--quiet', dest='verbosity',
                          action='store_const', const=0)

        group = parser.add_option_group('Options for connecting to the '
                                        'administrator')
        group.add_option('-h', '--host',
                          default=openvas.oaplib.ADMINISTRATOR_ADDRESS,
                          help=("Connect to administrator on host HOST "
                                "(default: %default)"))
        group.add_option('-p', '--port', type=int,
                          default=openvas.oaplib.ADMINISTRATOR_PORT,
                          help="Use port number PORT (default: %default)")
        group.add_option('-u', '--username', default=getpass.getuser(),
                          help="OAP username (default: current user's name)")
        group.add_option('-w', '--password',
                          help=("OAP password (use '-' to be prompted, "
                                "default: same as username)"))

        opts, args = parser.parse_args(argv[1:])

        if not (0 < opts.port < 65536):
            parser.error('Administrator port must be a number between 1 and 65535.')
        if opts.password is None:
            opts.password = opts.username
        elif opts.password == '-':
            opts.password = getpass.getpass('Enter password for openvas-administrator: ')

        self.verbosity = int(opts.verbosity)
        OAPTestBase._OAP_HOST = opts.host
        OAPTestBase._OAP_PORT = opts.port
        OAPTestBase._OAP_USER = opts.username
        OAPTestBase._OAP_PASSWD = opts.password
        
        if len(args) == 0 and self.defaultTest is None:
            self.test = self.testLoader.loadTestsFromModule(self.module)
            return
        if len(args) > 0:
            self.testNames = args
        else:
            self.testNames = (self.defaultTest,)
        self.createTests()

if __name__ == '__main__':
    main()
