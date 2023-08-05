# -*- coding: utf-8 -*-
#
# vim:set et:

import os
import iniparse
import tarfile

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from hgadmin.helpers import load_hgrc_from_template, touch_file


class Repository(models.Model):
    name = models.CharField(_(u'Name'), max_length=50, unique=True)
    old_name = models.CharField(_(u'Old name'), max_length=50, 
                                                    blank=True, null=True)

    description = models.CharField(_(u'Description'), max_length=50,
                                                    blank=True, null=True)

    contact = models.ForeignKey(User, null=True, blank=True)

    allow_push = models.ManyToManyField(User, null=True, blank=True,
                                related_name="%(class)s_allow_push_related")
    allow_push_all = models.BooleanField(_(u'Allow push all'), default=False)

    def __str__(self):
        return self.name

    def __unincode__(self):
        return self.name

    @property
    def repo_path(self):
        """Repository path"""
        return os.path.join(settings.HGWEBDIR_ROOT, self.name)

    @property
    def old_repo_path(self):
        if self.old_name:
            return os.path.join(settings.HGWEBDIR_ROOT, self.old_name)
        else:
            return self.repo_path

    @property
    def hgrc_path(self):
        """Repository config file"""
        return os.path.join(self.repo_path, '.hg', 'hgrc')

    def create_backup(self, backup=None):
        """Create repository backup archive"""
        if backup is None:
            backup = self.repo_path + '.tar.bz2'
        tar = tarfile.open(backup, 'w:bz2')
        tar.add(self.repo_path, self.name)
        tar.close()
        return backup

    def update_hgrc(self):
        """Sync model with config file"""
        path = self.hgrc_path

        if not os.path.exists(path):
            fp = load_hgrc_from_template(path)
        else:
            fp = file(path)

        ini = iniparse.INIConfig(fp)

        if self.contact:
            if self.contact.first_name and self.contact.last_name:
                contact = "%s %s" % (self.contact.first_name,
                                                    self.contact.last_name, )
            else:
                contact = self.contact.username

            if self.contact.email:
                contact += ' <' + self.contact.email + '>'

            ini.web.contact = contact
        else:
            try:
                del ini.web.contact
            except KeyError:
                pass

        if self.description:
            ini.web.description = self.description
        else:
            try:
                del ini.web.description
            except KeyError:
                pass

        if self.allow_push_all:
            ini.web.allow_push = u'*'
        else:
            ini.web.allow_push = u' '.join([u.username for u in
                                        self.allow_push.iterator()])

        try:
            with open(path, 'w') as f:
                f.write(str(ini))
        except IOError:
            raise IOError("Failed to write file: %s" % path)

        # tells apache to reload hgwebdir.wsgi
        try:
            touch_file(settings.HGWEBDIR_WSGI)
        except OSError:
            pass

    class Meta:
        verbose_name=_(u'repository')
        verbose_name_plural=_(u'repositories')
