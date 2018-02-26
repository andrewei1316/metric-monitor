#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil as cpu_ps
from base import MetricInfo
from tools.utils import namedtuple_to_dict


class CpuInfo(MetricInfo):
    prefix = "cpu_"

    def __init__(self, conf=None):
        MetricInfo.__init__(self)

    def get_time(self):
        data = []
        cpu_time = cpu_ps.cpu_times()
        data.append(namedtuple_to_dict(cpu_time, self.prefix, dict({'index': 'cpu-total'})))
        cpu_time = cpu_ps.cpu_times(percpu=True)
        for (i, c) in enumerate(cpu_time):
            data.append(namedtuple_to_dict(c, self.prefix, dict({'index': 'cpu-'+str(i)})))
        return data

    def get_time_percent(self):
        data = []
        cpu_time_percent = cpu_ps.cpu_times_percent()
        data.append(namedtuple_to_dict(cpu_time_percent, self.prefix, dict({'index': 'cpu-total'})))
        cpu_time_percent = cpu_ps.cpu_times(percpu=True)
        for (i, c) in enumerate(cpu_time_percent):
            data.append(namedtuple_to_dict(c, self.prefix, dict({'index': 'cpu-'+str(i)})))
        return data

    def get_frequency(self):
        data = []
        cpu_freq = cpu_ps.cpu_freq()
        data.append(namedtuple_to_dict(cpu_freq, self.prefix, dict({'index': 'cpu-total'})))
        cpu_freq = cpu_ps.cpu_freq(percpu=True)
        for (i, c) in enumerate(cpu_freq):
            data.append(namedtuple_to_dict(c, self.prefix, dict({'index': 'cpu-'+str(i)})))
        return data

    def get_state(self):
        cpu_stats = cpu_ps.cpu_stats()
        return namedtuple_to_dict(cpu_stats, self.prefix, dict({'index': 'cpu-total'}))

    def collect_data(self):
        data = []
        try:
            cpu_time = self.get_time()
            data.extend(cpu_time)
        except AttributeError as ex:
            print 'Warn: do not support get cpu time', ex

        try:
            cpu_time_percent = self.get_time_percent()
            data.extend(cpu_time_percent)
        except AttributeError as ex:
            print 'Warn: do not support get cpu time percent', ex

        try:
            cpu_freq = self.get_frequency()
            data.extend(cpu_freq)
        except AttributeError as ex:
            print 'Warn: do not support get cpu frequency', ex

        try:
            cpu_stats = self.get_state()
            data.append(cpu_stats)
        except AttributeError as ex:
            print 'Warn: do not support get cpu state', ex

        return data
