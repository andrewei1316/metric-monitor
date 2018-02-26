#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
from tools.models import *
from abc import ABCMeta, abstractmethod


class Sender(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def send(self, data_list):
        pass


def create_sender(conf):
    senders = dict()
    if not conf:
        return senders
    try:
        for c in conf.items(SENDER):
            if c[0] == HTTP:
                from sender.http import HttpSender
                senders[HTTP] = HttpSender(conf)
            else:
                print 'Warn: unknown sender type', c[0]
    except ConfigParser.NoSectionError:
        pass
    return senders

