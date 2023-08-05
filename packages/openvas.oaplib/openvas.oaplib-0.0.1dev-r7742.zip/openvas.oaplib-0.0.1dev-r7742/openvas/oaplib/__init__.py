#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
openvas.oaplib - An OAP (OpenVAS Administration Protocol) client interface for Python.

Results from OAP methods
---------------------------

In general all OAPClient methods return either a utf-8 encoded string
or an etree Element. If errors occur an exception subclassed from
`openvas.oaplib.Error` is raised.

Changing the ElementTree library
------------------------------------

``openvas.oaplib`` per default uses xml.etree.ElementTree (resp. it's
C-implementation xml.etree.cElementTree if available). If your
application is using another ElementTree library (e.g. lxml) you can
easily make openvas.oaplib using it by monkey-pathing openvas.oaplib::

  # at the very beginning of your application
  from lxml import etree
  import openvas.oaplib
  openvas.oaplib.etree = etree
  # need to comply to the ElementTree 1.2 interface
  etree.XMLTreeBuilder = etree.XMLParser

You may want to run the test suite to ensure it is really wroking,
though.
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
__version__ = "0.1.0"

import socket
import ssl

try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree


ADMINISTRATOR_ADDRESS = '127.0.0.1'
ADMINISTRATOR_PORT = 9393

# Available Roles
ROLES = ["User", "Admin"]

class Error(Exception):
    """Base class for OAP errors."""
    def __str__(self):
        return repr(self)

class _ErrorResponse(Error):
    def __init__(self, cmd, *args):
        if cmd.endswith('_response'):
            cmd = cmd[:-9]
        super(_ErrorResponse, self).__init__(cmd, *args)
        
    def __str__(self):
        return '%s %s' % self.args[1:3]

class ClientError(_ErrorResponse):
    """command issued could not be executed due to error made by the client"""
    
class ServerError(_ErrorResponse):
    """error occurred in the administrator during the processing of this command"""
    
class ResultError(Error):
    """Get invalid answer from Server"""
    def __str__(self):
        return 'Result Error: answer from command %s is invalid' % self.args

class AuthFailedError(Error):
    """Authentication failed."""


def XMLNode(tag, *kids, **attrs):
    n = etree.Element(tag, attrs)
    for k in kids:
        if isinstance(k, basestring):
            assert n.text is None
            n.text = k
        else:
            n.append(k)
    return n


class OAPClient(object):
    def __init__(self, host, port=ADMINISTRATOR_PORT, username=None, password=None):
        self.socket = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = None

    def open(self, username=None, password=None):
        """Open a connection to the administrator and authenticate the user."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = sock = ssl.wrap_socket(sock)
        sock.connect((self.host, self.port))
        self.authenticate(username, password)

    def close(self):
        """Close the connection to the administrator"""
        self.socket.close()
        self.socket = None

    def _send(self, data):
        """Send OAP data to the administrator and read the result.

        `data` may be either an unicode string, an utf-8 encoded
        string or an etree Element. The result is as an etree Element.
        """
        BLOCK_SIZE = 1024
        if etree.iselement(data):
            #print '>>>', etree.tostring(data)
            root = etree.ElementTree(data)
            root.write(self.socket, 'utf-8')
        else:
            if isinstance(data, unicode):
                data = data.encode('utf-8')
            self.socket.send(data)
        parser = etree.XMLTreeBuilder()
        while 1:
            res = self.socket.recv(BLOCK_SIZE)
            #print repr(res)
            parser.feed(res)
            if len(res) < BLOCK_SIZE:
                break
        root = parser.close()
        #print '<<<', etree.tostring(root)
        return root

    def _check_response(self, response):
        """Check the response read from the administrator.

        If the response status is 4xx a ClientError is raised, if the
        status is 5xx a ServerError is raised.
        """
        status = response.get('status')
        if status is None:
            raise RunTimeError('response is missing status: %s'
                               % etree.tostring(response))
        if status.startswith('4'):
            raise ClientError(response.tag, status,
                              response.get('status_text'))
        elif status.startswith('5'):
            raise ServerError(response.tag, status,
                              response.get('status_text'))
        return status

    def _text_command(self, request):
        response = self._send(request)
        self._check_response(response)
        return response.text

    def _xml_command(self, request):
        response = self._send(request)
        self._check_response(response)
        return response


    def __generic_get(self, type, name, element2dict):
        """
        Generic function for retrieving information using <get_XXX>.

        If 'name' is not given, retrieve all thingies. Result is a
        generator of dicts with the thingies datas.
        
        If 'name' is set, get only the thingy identified by its name.
        Result is a single dict with the thingies data.
        """
        request = XMLNode('get_%s' % type)
        if name is not None:
            request.set('name', name)
        response = self._xml_command(request)
        if name:
            return element2dict(response[0])
        else:
            return (element2dict(elem) for elem in response)


    # --- basic commands ---

    def authenticate(self, username=None, password=None):
        """
        Authenticate a user to the administrator.

        If username or password are not gives, the values passed when
        instanciating the object are used.

        Raises AuthFailedError if authentication failed due to wrong
        credentials.
        """
        if username is None:
            username = self.username
        if password is None:
            password = self.password
        request = XMLNode("authenticate",
                          XMLNode("credentials",
                                  XMLNode("username", username),
                                  XMLNode("password", password),
                                  ))
        try:
            self._text_command(request)
            # if not status: connection closed, raise error
        except ClientError:
            raise AuthFailedError(username)

    def xml(self, xmldata, xml_result=False):
        """Low-level interface to send OAP XML to the administrator.

        `xmldata` may be either an unicode string, an utf-8 encoded
        string or an etree Element. If `xml_result` is true, the
        result is returned as an etree Element, otherwise a unicode
        string is returned.

        Please see the modules documentation about how to change the
        ElementTree library used.
        """
        if xml_result:
            return self._xml_command(xmldata)
        else:
            return self._text_command(xmldata)

    def help(self):
        """
        Retrieve help from OAP server.
        """
        return self._text_command(XMLNode('help'))


    def get_version(self):
        """
        Retrieve protocol versions supported by the administrator.

        Returns two values: first is the preferred version, second
        element is a list of all versions (including the preferred
        one). Versions are strings, the order is as returned from the
        administrator.
        """
        response = self._xml_command(XMLNode('get_version'))
        preferred = None
        versions = []
        for ver in response.findall('version'):
            versions.append(ver.text)
            if ver.get('preferred'):
                if preferred:
                    raise ServerError("OAP command 'get_version' returned "
                                      "several preferred versions")
                preferred = ver.text
        if not preferred:
            raise ServerError("OAP command 'get_version' did not return "
                              "a preferred version")
        return preferred, versions

    # --- users ---

    def create_user(self, name, password, role, hosts):
        """
        Create a new user
        """
        request = XMLNode('create_user',
                          XMLNode('name', name),
                          XMLNode('password', password),
                          XMLNode('role', role),
                          XMLNode('hosts', hosts),
                          )
        self._text_command(request)

    def modify_user(self, name, password=None, role=None, hosts=None):
        """
        Modify an existing user
        """
        request = XMLNode('modify_user',
                          XMLNode('name', name)
                          )
        if password:
            request.append(XMLNode('password', password, modify="1"))
        else:
            request.append(XMLNode('password', modify="0"))
        if role:
            request.append(XMLNode('role', role))
        if hosts:
            request.append(XMLNode('hosts', hosts))
        self._text_command(request)


    def get_users(self, name=None):
        """
        Get information about user(s).

        If 'name' is not given, retrieve all users. Result is a
        generator of dicts with the users datas.
        
        If 'name' is set, get only the users identified by its name.
        Result is a single dict with the users data.
        """

        def user2dict(element):
            entry = dict((elem.tag, elem.text) for elem in element)
            # todo: find a better solution for this
            entry['hosts_allow'] = element.find('hosts').get('allow')
            # work around asymetry in openvas-administrator
            if entry['role'] == "Administrator":
                entry['role'] = "Admin"
            return entry

        return self.__generic_get('users', name, user2dict)


    def delete_user(self, name):
        """
        Delete an user identified by his name
        """
        request = XMLNode('delete_user', name=name)
        return self._text_command(request)


    # --- configs ---

    def describe_feed(self):
        """
        Get details of the NVT feed this administrator uses.

        Returns a dict containing the information.
        """

        def feed2dict(element):
            # todo: currently_syncing
            entry = dict((elem.tag, elem.text) for elem in element)
            syncing = element.find('currently_syncing')
            if syncing is not None:
                entry['currently_syncing'] = feed2dict(syncing)
            return entry

        request = XMLNode('describe_feed')
        res = self._xml_command(request)
        return feed2dict(res.find('feed'))

    def sync_feed(self):
        """
        Synchronize with an NVT feed
        """
        request = XMLNode('sync_feed')
        return self._text_command(request)


    def describe_auth(self):
        """
        Get details about the used authentication methods
        """
        request = XMLNode('describe_auth')
        return self._text_command(request).decode('base64')


    def get_settings(self, name=None):
        """
        Get information about settings
        """
        request = XMLNode('get_settings')
        res = self._xml_command(request)
        settings = []
        for scanner_settings in res.findall('scanner_settings'):
            # copy attributes
            scan_setting = dict(scanner_settings.items())
            setting_items = scan_setting['items'] = {}
            for setting in scanner_settings.findall('setting'):
                setting_items[setting.get('name')] = setting.text
            settings.append(scan_setting)
        return settings
