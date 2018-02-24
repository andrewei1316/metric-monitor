#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil as disk_ps
from tools.utils import namedtuple_to_dict


class DiskInfo:
    disk_prefix = "disk_"
    diskio_prefix = "diskio_"

    def __init__(self, conf=None):
        pass

    def get_partitions(self):
        data = []
        disk_part = disk_ps.disk_partitions()
        for d in disk_part:
            data.append(namedtuple_to_dict(d, self.disk_prefix))
        return data

    def get_usage(self, path_list):
        data = []
        for p in path_list:
            disk_usage = disk_ps.disk_usage(p)
            data.append(namedtuple_to_dict(disk_usage, self.disk_prefix, dict({'mountpoint': p})))
        return data

    def get_io_counters(self):
        data = []
        diskio_counters = disk_ps.disk_io_counters(perdisk=False)
        data.append(namedtuple_to_dict(diskio_counters, self.diskio_prefix, dict({'device': 'disk-total'})))
        diskio_counters = disk_ps.disk_io_counters(perdisk=True)
        for (k, v) in diskio_counters.items():
            data.append(namedtuple_to_dict(v, self.diskio_prefix, dict({'device': k})))
        return data

    def collect_data(self):
        data = []

        disk_part = self.get_partitions()
        data.extend(disk_part)

        path_list = []
        for p in disk_part:
            try:
                path_list.append(p[self.disk_prefix+'mountpoint'])
            except KeyError:
                print 'Warn: disk partition has no key[mountpoint]'
        disk_usage = self.get_usage(path_list=path_list)
        data.extend(disk_usage)

        diskio_counters = self.get_io_counters()
        data.extend(diskio_counters)

        return data
