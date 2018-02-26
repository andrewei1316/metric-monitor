#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import psutil as sys_ps
from tools.utils import namedtuple_to_dict


class SystemInfo:
    prefix = 'system_'

    def __init__(self, conf=None):
        pass

    def get_base_info(self):
        """ 获取 启动日期、load、cpu 核数等"""
        boot_time = sys_ps.boot_time()
        load1, load5, load15 = os.getloadavg()
        cpu_count = sys_ps.cpu_count(logical=False)
        cpu_count_logical = sys_ps.cpu_count(logical=True)
        data = {
            'system_boot_time': boot_time,
            'system_boot_time_str': datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S"),
            'system_load1': load1,
            'system_load5': load5,
            'system_load15': load15,
            'cpu_count': cpu_count,
            'cpu_count_logical': cpu_count_logical
        }
        return data

    def get_users(self):
        data = []
        users = sys_ps.users()
        for u in users:
            data.append(namedtuple_to_dict(u, self.prefix, dict({'type': 'user'})))
        return data

    def collect_data(self):
        data = []

        try:
            base_info = self.get_base_info()
            data.append(base_info)
        except AttributeError as ex:
            print 'Warn: do not get system base information', ex

        try:
            users = self.get_users()
            data.extend(users)
        except AttributeError as ex:
            print 'Warn: do not get system users', ex

        return data
