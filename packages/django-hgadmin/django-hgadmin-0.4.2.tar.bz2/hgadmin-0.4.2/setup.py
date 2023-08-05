#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 et:

from os.path import join, dirname
from setuptools import setup, find_packages
import hgadmin

def desc():
    return open(join(dirname(__file__), 'README')).read()

setup(
    name="django-hgadmin",
    description="""Mercurial repository administaration tool""",
    long_description=desc(),
    license="BSD",
    version = hgadmin.__version__,
    author = hgadmin.__author__,
    author_email = hgadmin.__email__,
    url = "http://vehq.ru/project/HGAdmin",
    download_url = 'http://hg.vehq.ru/hgadmin/archive/%s.tar.bz2' % hgadmin.__version__,
    keywords = ['Django', 'Mercurial', 'tool'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
    ],
    packages=find_packages(),
    package_data = {'hgadmin': ['templates/hgadmin/*', 'locale/*/*/*']},
    install_requires = ['iniparse'],
    platforms = 'any',
)
