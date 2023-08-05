# -*- coding: utf-8 -*-

# Copyright (c) 2010, Webreactor - Marcin Lulek <info@webreactor.eu>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sqlalchemy as sa
import reactorauth

# dummy translation marker
_ = lambda s: s

class HasPermission(reactorauth.BaseCondition):
    
    def __init__(self, *args, **kwargs):
        self.permissions = args
        self.message = kwargs.get('message', u'User must have permission:')
    
    def check(self):
        from pylons import request
        if 'REMOTE_USER' in request.environ:
            for permission in request.user.permissions:
                if permission.name in self.permissions:
                    return True
        raise reactorauth.NotValidAuth(_(self.message), information=self.permissions)


class HasPermissions(reactorauth.BaseCondition):

    def __init__(self, *args, **kwargs):
        self.permissions = args
        self.message = kwargs.get('message', u'User must have permissions:')
    
    def check(self):
        from pylons import request
        if 'REMOTE_USER' in request.environ:
            met_permissions = 0
            for permission in request.user.permissions:
                if permission.name in self.permissions:
                    met_permissions += 1
            if met_permissions == len(self.permissions):
                return True
        raise reactorauth.NotValidAuth(_(self.message), information=self.permissions)


class InGroups(reactorauth.BaseCondition):
    
    def __init__(self, *args, **kwargs):
        self.groups = args
        self.message = kwargs.get('message', u'User must belong to groups:')
    
    def check(self):
        from pylons import request
        if 'REMOTE_USER' in request.environ:
            met_groups = 0
            for group in request.user.groups:
                if group.name in self.groups:
                    met_groups += 1
            if met_groups == len(self.groups):
                return True
        raise reactorauth.NotValidAuth(_(self.message), information=self.groups)


class InOneOfGroups(reactorauth.BaseCondition):

    def __init__(self, *args, **kwargs):
        self.groups = args
        self.message = kwargs.get('message', u'User must belong to at least one of groups:')
    
    def check(self):
        from pylons import request
        if 'REMOTE_USER' in request.environ:
            for group in request.user.groups:
                if group.name in self.groups:
                    return True
        raise reactorauth.NotValidAuth(_(self.message), information=self.groups)
    

class IsLogged(reactorauth.BaseCondition):
    
    def __init__(self, message=u'User needs to be logged in'):
        self.message = message
    
    def check(self):
        from pylons import request
        if 'REMOTE_USER' in request.environ:
            return True
        raise reactorauth.NotValidAuth(_(self.message))
