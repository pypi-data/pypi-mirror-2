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

__all__ = ['NotValidAuth', 'BaseCondition', 'AllMet', 'OneMet', 'Not',
           'condition', 'condition_view_helper', 'TextConditionErrorParser',
           'HTMLBuilderListConditionErrorParser', 'HTMLListConditionErrorParser'
           ]

from decorator import decorator

# dummy translation marker
_ = lambda s: s

class NotValidAuth(Exception):
    """ Base exception class that can gather information about nested checks"""
    
    def __init__(self, message, conditions=None, information=None):
        self.message = message
        self.conditions = conditions
        self.information = information
        
    def __str__(self):
        return '%s, %s, %s' % (self.message, self.conditions, self.information)


def condition(valid, handler):
    """ This is main decorator that is used for protecting actions
    and controllers.
    
    example usage: @condition(IsLogged(), no_auth_handler)
    
    no_auth_handler should be any callable that receives exception
    as argument, and can be used to handle situation when the check failed.
    example:
    
        def no_auth_handler(exception):
            parser = HTMLBuilderListConditionErrorParser()
            h.flash(parser.parse(exception),
                    'warning', ignore_duplicate=True)
            if request.is_xhr:
                abort(403)
            else:
                redirect(url('/'))
    
    Remember that you can use checks inside an action directly and catch
    NotValidAuth exception
    
    """
    
    def validate(func, self, *args, **kwargs):
        try:
            valid.check(org_args=args, org_kwargs=kwargs)
        except NotValidAuth, e:
            return handler(e)
        return func(self, *args, **kwargs)
    return decorator(validate)


class BaseCondition(object):
    """ This is base class :P maybe it will handle translations in future, for now one could extend one of parsers to hook in gettext"""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('Not implemented yet')
    
    def check(self, org_args=None, org_kwargs=None):
        raise NotImplementedError('Not implemented yet')

class AllMet(BaseCondition):
    """ Condition class that required every check to successfully evaluate.
    
    Example usage:
        
        @condition(AllMet(IsLogged(),OwnerOfObjectCheck(),HasPermission('editor')), no_auth_handler)
    """
    
    def __init__(self, *args, **kwargs):
        self.conditions = args
        self.message = kwargs.get('message', u'All of these conditions have to be met:')
    
    def check(self, org_args=None, org_kwargs=None):
        sub_conditions = []
        valid = True
        for condition in self.conditions:
            try:
                condition.check(org_args, org_kwargs)
            except NotValidAuth, e:
                valid = False
                sub_conditions.append(e)
        if valid:
            return True
        raise NotValidAuth(_(self.message), sub_conditions)
    

class OneMet(BaseCondition):
    """ Condition class that requires at least one check to pass successfuly.
    
    Example usage:
        
        @condition(OneMet(InGroup('administrators'),HasPermission('moderator')), no_auth_handler)
    """
      
    def __init__(self, *args, **kwargs):
        self.conditions = args
        self.message = kwargs.get('message', u'At least one of these conditions have to be met:')
    
    def check(self, org_args=None, org_kwargs=None):
        sub_conditions = []
        valid = False
        for condition in self.conditions:
            try:
                condition.check(org_args, org_kwargs)
                return True
            except NotValidAuth, e:
                sub_conditions.append(e)
        raise NotValidAuth(_(self.message), sub_conditions)


class Not(BaseCondition):
    """ Condition class that requires at least one check to pass sucessfuly.
    
    Example usage:
        
        @condition(OneMet(InGroup('administrators'),HasPermission('moderator')), no_auth_handler)
    """
    
    def __init__(self, *args, **kwargs):
        self.conditions = args
        self.message = kwargs.get('message', u'All of these conditions have to be not met:')
    
    def check(self, org_args=None, org_kwargs=None):
        sub_conditions = []
        valid = True
        for condition in self.conditions:
            try:
                condition.check(org_args, org_kwargs)
                valid = False
            except NotValidAuth, e:
                sub_conditions.append(e)
        if valid:
            return True
        raise NotValidAuth(_(self.message), sub_conditions)


def condition_view_helper(condition):
    """ helpful when one wants to check if user has a permission inside a view,
    and alter it based on that """
    
    try:
        condition.check()
        return True
    except (NotValidAuth,), e:
        pass
    return False

class TextConditionErrorParser(object):
    """ A Simple text parser to generate text information on why condition
    checks failed"""
    
    def __init__(self):
        self.messages = []
    
    def parse(self, exception):
        self.messages.append(exception.message)
        if exception.information:
            self.messages[-1] = '%s %s' % (self.messages[-1], ', '.join(exception.information))  
        if hasattr(exception, 'conditions') and exception.conditions:
            for condition in exception.conditions:
                self.parse(condition)
        return ' '.join(self.messages)
    
class HTMLBuilderListConditionErrorParser(object):
    """ Webhelpers based parser that performs some string concatenations to
    produce html list with information why checks failed"""
    
    def parse(self, exception):
        from webhelpers.html import HTML
        information_list = []
        if exception.information:
            for text in exception.information:
                information_list.append(HTML.li(text))                                            
        information_ul = HTML.ul(*information_list)
        
        nested_uls = []
        if hasattr(exception, 'conditions') and exception.conditions:
            for condition in exception.conditions:
                nested_uls.append(self.parse(condition))
        
        return HTML.ul(
                       exception.message,
                       information_ul,
                       *nested_uls
                       )  
        self.messages.append('</li></ul>')
        
    
class HTMLListConditionErrorParser(object):
    """ Very evil parser that performs some string concatenations to produce
    html list with information why checks failed - IT MAY BE UNSAFE"""
    
    def __init__(self):
        self.messages = []
    
    def parse(self, exception):
        from cgi import escape
        self.messages.append('<ul><li>')
        self.messages.append(escape(exception.message))
        if exception.information:
            self.messages[-1] = '%s <ul><li>%s</li></ul>' % (self.messages[-1], ',</li><li>'.join([escape(info) for info in exception.information]))  
        if hasattr(exception, 'conditions') and exception.conditions:
            for condition in exception.conditions:
                self.parse(condition)
        self.messages.append('</li></ul>')
        return ' '.join(self.messages)
