#!/usr/bin/python
# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.beaker.interfaces import ISessionConfig


class ImmutableDict(dict):
    """A dict that can be updated only through the `update` or
    `setdefault` methods.
    """
    def __setitem__(self, key, value):
        raise NotImplementedError(
            'This dict cannot be altered through direct assignation')

    def __hash__(self):
        items = self.items()
        res = hash(items[0])
        for item in items[1:]:
            res ^= hash(item)
        return res


DEFAUT_CONFIG = ImmutableDict(
    data_dir=None,
    invalidate_corrupt=True,
    key='beaker.session.id',
    log_file=None,
    secret="DolmenRocks",
    timeout=600,
    type="cookie",
    validate_key="thisCouldBeChanged")


grok.global_utility(DEFAUT_CONFIG, provides=ISessionConfig, direct=True)
