#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
from tools.models import *
from abc import ABCMeta, abstractmethod


class MetricInfo(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def collect_data(self):
        pass


def create_metric(conf):
    metrics = dict()
    if not conf:
        return metrics
    try:
        for c in conf.items(METRICS):
            if c[0] == CPU and c[1]:
                from metrics.cpu import CpuInfo
                metrics[CPU] = CpuInfo(conf)
            elif c[0] == DISK and c[1]:
                from metrics.disk import DiskInfo
                metrics[DISK] = DiskInfo(conf)
            elif c[0] == MEMORY and c[1]:
                from metrics.memory import MemoryInfo
                metrics[MEMORY] = MemoryInfo(conf)
            elif c[0] == NET and c[1]:
                from metrics.net import NetworkInfo
                metrics[NET] = NetworkInfo(conf)
            elif c[0] == PROCSTAT and c[1]:
                from metrics.procstat import ProcInfo
                metrics[PROCSTAT] = ProcInfo(conf)
            elif c[0] == SENSOR and c[1]:
                from metrics.sensor import SensorInfo
                metrics[SENDER] = SensorInfo(conf)
            elif c[0] == SYSTEM and c[1]:
                from metrics.system import SystemInfo
                metrics[SYSTEM] = SystemInfo(conf)
            else:
                print 'Warn: unknown metric type', c[0]
    except ConfigParser.NoSectionError:
        pass
    return metrics

