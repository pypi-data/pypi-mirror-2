# -*- mode: python -*-
# vim:set ft=python et:
#
# WSGI Auth script
#
# Require Apache mod_wsgi>=2.3
# 
# Apache config:
#
#  AuthName "repository"
#  AuthType Basic
#  AuthBasicProvider wsgi
#  WSGIAuthUserScript /path/to/your/auth.wsgi
#


import sys
import os
import os.path

if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

def check_password(environ, user, password):
    db.reset_queries()
    
    err = environ.get('wsgi.errors', sys.stderr)

    try: 
        try: 
            user = User.objects.get(username=user, is_active=True)
        except User.DoesNotExist: 
            err.write("%s: User '%s' does not exist\n" % (
                    __file__, user, ))
            return None
        
        #try:
        #    import hgadmin
        #except ImportError:
        #    err.write("%s: Can't import module 'hgadmin' [%s]\n" % (
        #        __file__, ' '.join(sys.path), ))
        #    return None

        if not user.has_perm('hgadmin.change_repository'):
            err.write("%s: User '%s' have't permissions for push\n" % (
                __file__, user.username, ))
            return None

        if user.check_password(password):
            return True
        else:
            err.write("%s: User '%s': incorrect password\n" % (
                __file__, user.username, ))
            return False
    finally: 
        db.connection.close()

