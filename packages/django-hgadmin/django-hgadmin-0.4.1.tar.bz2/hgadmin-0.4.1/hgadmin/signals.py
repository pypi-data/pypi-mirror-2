# -*- coding: utf-8 -*-
#
# vim:set et:

import os
import shutil

from mercurial import ui, hg

from django.conf import settings
from hgadmin.models import Repository


def check_rename(sender, instance, **kwargs):
    try:
        old = Repository.objects.get(pk=instance.pk)
        if old.name != instance.name:
            instance.old_name = old.name
    except Repository.DoesNotExist:
        pass


def rename_repo(sender, instance, **kwargs):
    if instance.old_name and os.path.isdir(instance.old_repo_path):
        return shutil.move(instance.old_repo_path, instance.repo_path)


def update_repo(sender, instance, **kwargs):
    """Updates repository config"""
    instance.update_hgrc()


def create_repo(instance, created, **kwargs):
    """Creates new repository"""
    if not created:
        return
    if not os.path.isdir(instance.repo_path):
        # old ui:
        #u = ui.ui(report_untrusted=False, interactive=False, quiet=True)
        u = ui.ui()
        hg.repository(u, instance.repo_path, create=True)
        return True
    else:
        raise ValueError("Invalid: %s already exists for this project" %
                                                    instance.name_short)


def delete_repo(sender, instance, **kwargs):
    """Destroy repo"""
    if os.path.isdir(instance.repo_path):
        instance.create_backup()
        return shutil.rmtree(instance.repo_path)
