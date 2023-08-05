reactorauth
============

Set of decorators for authorization + small list of condition checks for pylons.

example usage:

    @condition(IsLogged(), no_auth_handler)
    
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


reactorauth is BSD licensed, consult LICENSE for details. 

Installation and Setup
======================

Install ``reactorauth`` using easy_install::

    easy_install reactorauth