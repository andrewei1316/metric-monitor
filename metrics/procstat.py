#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rfc3339
import datetime
import psutil as proc_ps
from base import MetricInfo
from tools.utils import namedtuple_to_dict


class ProcInfo(MetricInfo):
    prefix = "proc_"

    def __init__(self, conf=None):
        MetricInfo.__init__(self)

    def get_proc_info(self, proc):
        d = dict()
        try:
            d[self.prefix + 'pid'] = proc.pid
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'status'] = proc.status()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'name'] = proc.name()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'exe'] = proc.exe()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'cmdline'] = ' '.join(proc.cmdline())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'create_time'] = rfc3339.rfc3339(datetime.datetime.fromtimestamp(proc.create_time()))
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'ppid'] = namedtuple_to_dict(proc.parent())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'cmd'] = proc.cmd()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'nice'] = proc.nice()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'ionice'] = namedtuple_to_dict(proc.ionice())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'io_counter'] = namedtuple_to_dict(proc.io_counters())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'num_ctx_switches'] = namedtuple_to_dict(proc.num_ctx_switches())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'num_fds'] = proc.num_fds()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'num_handles'] = proc.num_handles()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'num_threads'] = proc.num_threads()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'threads'] = proc.threads()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'cpu_times'] = namedtuple_to_dict(proc.cpu_times())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'cpu_percent'] = proc.cpu_percent()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'cpu_num'] = proc.cpu_num()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'memory_info'] = namedtuple_to_dict(proc.memory_full_info())
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'memory_percent'] = proc.memory_percent()
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'open_files'] = [namedtuple_to_dict(tup) for tup in proc.open_files()]
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        try:
            d[self.prefix + 'connections'] = [namedtuple_to_dict(tup) for tup in proc.connections()]
        except AttributeError:
            pass
        except proc_ps.AccessDenied:
            pass
        return d

    def get_data(self):
        data = []
        proc_num = {
            self.prefix+proc_ps.STATUS_DEAD: 0,
            self.prefix+proc_ps.STATUS_IDLE: 0,
            self.prefix+proc_ps.STATUS_LOCKED: 0,
            self.prefix+proc_ps.STATUS_RUNNING: 0,
            self.prefix+proc_ps.STATUS_SLEEPING: 0,
            self.prefix+proc_ps.STATUS_STOPPED: 0,
            self.prefix+proc_ps.STATUS_WAITING: 0,
            self.prefix+proc_ps.STATUS_WAKING: 0,
            self.prefix+proc_ps.STATUS_ZOMBIE: 0,
            self.prefix+proc_ps.STATUS_DISK_SLEEP: 0,
            self.prefix+proc_ps.STATUS_TRACING_STOP: 0,
        }
        for proc in self.process_iter:
            with proc.oneshot():
                try:
                    proc_num[proc.status()] += 1
                except KeyError:
                    pass
                data.append(self.get_proc_info(proc))
        data.append(proc_num)
        return data

    def collect_data(self):
        self.process_iter = proc_ps.process_iter()
        return self.get_data()

