# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------- #
# Copyright 2010, Łukasz Oleś                                                #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
#--------------------------------------------------------------------------- #
import xmlrpclib
import os
import hashlib
import re
import socket

from host import Host, HostPool
from virtualmachine import VirtualMachine, VirtualMachinePool
from cluster import Cluster, ClusterPool
from user import User, UserPool
from image import Image, ImagePool
from virtualnetwork import VirtualNetwork, VirtualNetworkPool


ALL = -2
CONNECTED = -1


class OpenNebulaException(Exception):
    pass


class Client(object):
    '''
    The client class, represents the connection with the core and handles the
    xml-rpc calls(see http://www.opennebula.org/documentation:rel2.0:api)
    '''
    DEFAULT_ONE_AUTH = "~/.one/one_auth"
    ONE_AUTH_RE = re.compile('^(.+?):(.+)$')
    DEFAULT_ONE_ADDRESS = "http://localhost:2633/RPC2"

    def __init__(self, secret=None, address=None):
        if secret:
            one_secret = secret
        elif os.environ.has_key("ONE_AUTH") and os.environ["ONE_AUTH"]:
            one_auth = os.path.expanduser(os.environ["ONE_AUTH"])
            with open(one_auth) as f:
                one_secret = f.read().strip()
        elif os.path.exists(os.path.expanduser(self.DEFAULT_ONE_AUTH)):
            with open(os.path.expanduser(self.DEFAULT_ONE_AUTH)) as f:
                one_secret = f.read().strip()
        else:
            raise OpenNebulaException('ONE_AUTH file not present')

        one_secret = self.ONE_AUTH_RE.match(one_secret)
        if one_secret:
            user = one_secret.groups()[0]
            password = one_secret.groups()[1]
        else:
            raise OpenNebulaException("Authorization file malformed")

        if password.startswith('plain:'):
            password = password.split(':', 1)[1]
        else:
            password = hashlib.sha1(password).hexdigest()
        self.one_auth = '{0}:{1}'.format(user, password)

        if address:
            self.one_address = address
        elif os.environ.has_key("ONE_XMLRPC") and os.environ["ONE_XMLRPC"]:
            self.one_address = os.environ["ONE_XMLRPC"]
        else:
            self.one_address = self.DEFAULT_ONE_ADDRESS

        self.server = xmlrpclib.ServerProxy(self.one_address)

    def call(self, function, *args):
        '''
        Calls rpc function.

        Arguments

        ``function``
           OpenNebula xmlrpc funtcion name (without preceding 'one.')

        ``args``
           function arguments

        '''
        try:
            func = getattr(self.server.one, function)
            ret = func(self.one_auth, *args)
            try:
                return_code, data = ret
            except ValueError:
                data = ''
                return_code = ret[0]
        except socket.error, e:
            #connection error
            raise e
        if not return_code:
            raise OpenNebulaException(data)
        return data

__all__ = [Client, OpenNebulaException, Host, HostPool, VirtualMachine,
        VirtualMachinePool, Cluster, ClusterPool, User, UserPool,
        Image, ImagePool, VirtualNetwork, VirtualNetworkPool, ALL, CONNECTED]

