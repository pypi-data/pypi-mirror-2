# -*- coding: utf-8 -*-
#
# vim:set et:

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from hgadmin.models import Repository
from hgadmin.helpers import signals
from hgadmin.signals import check_rename, rename_repo, \
                        create_repo, update_repo, delete_repo


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'contact', )
    list_filter = ('contact', )

##
# register admin
#
admin.site.register(Repository, RepositoryAdmin)

##
# register signals
#
signals.pre_save(sender=Repository)(check_rename)
signals.post_save(sender=Repository)(create_repo)
signals.post_save(sender=Repository)(rename_repo)
signals.post_save(sender=Repository)(update_repo)

if settings.HGADMIN_ALLOW_REMOVE:
    signals.post_delete(sender=Repository)(delete_repo)
