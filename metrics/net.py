#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil as net_ps
from base import MetricInfo
from tools.utils import namedtuple_to_dict


class NetworkInfo(MetricInfo):
    prefix = 'net_'

    def __init__(self, conf=None):
        MetricInfo.__init__(self)
        pass

    def get_io_counters(self):
        data = []
        io_counters = net_ps.net_io_counters()
        data.append(namedtuple_to_dict(io_counters, self.prefix, dict({'interface': 'total'})))

        io_counters = net_ps.net_io_counters(pernic=True)
        for (k, i) in io_counters.items():
            data.append(namedtuple_to_dict(i, self.prefix, dict({'interface': k})))
        return data

    def get_connections(self):
        data = []
        inter_conn = net_ps.net_connections()
        for ic in inter_conn:
            data.append(namedtuple_to_dict(ic, self.prefix))
        return data

    def get_if_addrs(self):
        data = []
        if_addrs = net_ps.net_if_addrs()
        for (k, ia) in if_addrs.items():
            for i in ia:
                data.append(namedtuple_to_dict(i, self.prefix, dict({'interface': k})))
        return data

    def get_if_stats(self):
        data = []
        if_stats = net_ps.net_if_stats()
        for (k, iss) in if_stats.items():
            data.append(namedtuple_to_dict(iss, self.prefix, dict({'interface': k})))
        return data

    def collect_data(self):
        data = []

        try:
            io_counters = self.get_io_counters()
            data.extend(io_counters)
        except AttributeError, ex:
            print 'Warn: do not support get net io counters', ex

        try:
            inter_connections = self.get_connections()
            data.extend(inter_connections)
        except AttributeError as ex:
            print 'Warn: do not support get net interface connections', ex
        except net_ps.AccessDenied:
            print 'Warn: network connnections information should run as root'

        try:
            if_addrs = self.get_if_addrs()
            data.extend(if_addrs)
        except AttributeError as ex:
            print 'Warn: do not support get if addrs', ex

        try:
            if_stats = self.get_if_stats()
            data.extend(if_stats)
        except AttributeError as ex:
            print 'Warn: do not support get if stats', ex

        return data

