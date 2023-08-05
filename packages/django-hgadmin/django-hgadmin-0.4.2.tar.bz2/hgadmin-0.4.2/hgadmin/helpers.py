# -*- coding: utf-8 -*-
# vim:set et:
#
# Copy from byteflow (http://byteflow.su)
#   /apps/lib
#

import os
import iniparse
from cStringIO import StringIO

from django.conf import settings
from django.db.models import signals as signalmodule
from django.template.loader import render_to_string


def touch_file(path):
    "updates mtime"
    os.utime(path, None)


def load_hgrc_from_template(path):
    fp = StringIO(render_to_string('hgadmin/hgrc.txt', {}).encode('utf-8'))
    try:
        hgweb = iniparse.INIConfig(file(settings.HGWEBDIR_CONF))
        hgrc = iniparse.INIConfig(fp)

        # copy some sections from hgweb.config
        for sect in filter(lambda s: s in ('web', 'extensions', ),
                                                            list(hgweb)):
            for var in list(hgweb[sect]):
                hgrc[sect][var] = hgweb[sect][var]

        fp = StringIO(str(hgrc))
    finally:
        fp.reset()
    return fp


class Signals(object):
    '''
    Convenient wrapper for working with Django's signals (or any other
    implementation using same API).

    Example of usage::

       signals.register_signal(siginstance, signame)

       # connect to registered signal
       @signals.signame(sender=YourModel)
       def sighandler(instance, **kwargs):
           perform(instance)

       # connect to any signal
       @signals(siginstance, sender=YourModel)
       def sighandler(instance, **kwargs):
           perform(instance)

    In any case defined function will remain as is, without any changes.

    (c) 2009 Alexander Solovyov, new BSD License
    '''

    def __init__(self):
        self._signals = {}

    def __getattr__(self, name):
        return self._connect(self._signals[name])

    def __call__(self, signal, **kwargs):

        def inner(func):
            signal.connect(func, **kwargs)
            return func
        return inner

    def _connect(self, signal):

        def wrapper(**kwargs):
            return self(signal, **kwargs)
        return wrapper

    def register_signal(self, signal, name):
        self._signals[name] = signal

signals = Signals()

# register all Django's default signals
for k, v in signalmodule.__dict__.iteritems():
    # that's hardcode, but IMHO it's better than isinstance
    if not k.startswith('__') and k != 'Signal':
        signals.register_signal(v, k)
