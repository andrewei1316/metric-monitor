#!/usr/bin/env python
# -*- coding: utf-8 -*-


def namedtuple_to_dict(tup, prefix="", tag={}):
    data = dict()
    d = dict(tup._asdict())
    for (k, v) in d.items():
        data[prefix+k] = v
    for (k, v) in tag.items():
        data[prefix+k] = v
    return data
