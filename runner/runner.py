#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import rfc3339
import ConfigParser
from tools.models import *
from sender.base import create_sender
from metrics.base import create_metric


class Runner(object):
    metrics = {}
    senders = {}
    interval = 3
    add_hostname = True
    add_timestamp = True

    def __init__(self, conf):
        try:
            interval = conf.getint(RUNNER, INTERVAL)
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass
        else:
            self.interval = interval
        try:
            add_hostname = conf.getboolean(RUNNER, HOSTNAME)
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass
        else:
            self.add_hostname = add_hostname
        try:
            add_timestamp = conf.getboolean(RUNNER, TIMESTAMP)
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass
        else:
            self.add_timestamp = add_timestamp

        if self.add_hostname:
            self.hostname = socket.gethostname()

        self.metrics = create_metric(conf)
        self.senders = create_sender(conf)

    def run(self):
        while True:
            data = []
            timestamp = rfc3339.rfc3339(time.time(), utc=True, use_system_timezone=False)
            for (k, m) in self.metrics.items():
                try:
                    tmp_data = m.collect_data()
                    for d in tmp_data:
                        d[METRICS_TYPE] = k
                        if self.add_timestamp:
                            d[TIMESTAMP] = timestamp
                        if self.add_hostname:
                            d[HOSTNAME] = self.hostname
                        data.append(d)
                except AttributeError:
                    print 'Warn:', k, 'has no attr collect_data()'

            for (k, s) in self.senders.items():
                try:
                    s.send(data)
                except AttributeError:
                    print 'Warn:', k, 'has no attr send(data)'
            time.sleep(self.interval)
