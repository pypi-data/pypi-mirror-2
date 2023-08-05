# -*- coding: utf-8 -*-
# vim:set et:

import sys
import os

from mercurial import util
from iniparse import INIConfig
from iniparse.config import Undefined

from django.conf import settings
from django.contrib.auth.models import User

from hgadmin.models import Repository
from hgadmin.helpers import signals
from hgadmin import models as hgadmin_app


@signals.post_syncdb(sender=hgadmin_app)
def load_repos_data(app, created_models, verbosity, **kwargs):

    def ini_string(string):
        if isinstance(string, Undefined):
            return ''
        else:
            return string

    roothead = settings.HGWEBDIR_ROOT

    for path in util.walkrepos(roothead, followsym=True, recurse=True):
        name = util.pconvert(path[len(roothead):]).strip('/')
        repo, status = Repository.objects.get_or_create(name=name)

        try:
            hgrc = INIConfig(file(repo.hgrc_path))

            repo.description = ini_string(hgrc.web.description)

            try:
                repo.contact = User.objects.get(email=util.email(
                    ini_string(hgrc.web.contact)))
            except User.DoesNotExist:
                pass

            allow_push_list = ini_string(hgrc.web.allow_push).split()
            if '*' in allow_push_list:
                repo.allow_push_all = True
            else:
                repo.allow_push_all = False
                repo.save()
                for username in allow_push_list:
                    try:
                        user = User.objects.get(username=username)
                        repo.allow_push.add(user)
                    except User.DoesNotExist:
                        print >> sys.stderr, "Hgadmin: '%s' repo: unknown" \
                                "user in allow_push: %s" % (name, username, )
        except IOError:
            print >> sys.stderr, "File '%s' does not exist" % repo.hgrc_path
        except AttributeError:
            pass # section web does'nt exist
        finally:
            repo.save()
