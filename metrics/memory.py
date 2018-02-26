#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil as mem_ps
from tools.utils import namedtuple_to_dict


class MemoryInfo:
    memPrefix = "mem_"
    swapPrefix = "swap_"

    def __init__(self, conf=None):
        pass

    def get_virtual_memory(self):
        vir_mem = mem_ps.virtual_memory()
        return namedtuple_to_dict(vir_mem, self.memPrefix)

    def get_swap_memory(self):
        swap_mem = mem_ps.swap_memory()
        return namedtuple_to_dict(swap_mem, self.swapPrefix)

    def collect_data(self):
        data = []

        try:
            mem = self.get_virtual_memory()
            data.append(mem)
        except AttributeError as ex:
            print 'Warn: do not get virtual memory', ex

        try:
            swap = self.get_swap_memory()
            data.append(swap)
        except AttributeError as ex:
            print 'Warn: do not get swap memory', ex

        return data
