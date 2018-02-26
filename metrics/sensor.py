#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil as sensor_ps
from tools.utils import namedtuple_to_dict


class SensorInfo:
    prefix = "sensor_"

    def __init__(self, conf=None):
        pass

    def get_temperatures(self):
        data = []
        temperatures = sensor_ps.sensors_temperatures()
        for (k, temp) in temperatures.items():
            for t in temp:
                data.append(namedtuple_to_dict(t, self.prefix, dict({'type': 'temperature', 'item': k})))
        return data

    def get_fans(self):
        data = []
        fans = sensor_ps.sensors_fans()
        for (k, fan) in fans.items():
            for f in fan:
                data.append(namedtuple_to_dict(f, self.prefix, dict({'type': 'fan', 'item': k})))
        return data

    def get_battery(self):
        data = []
        battery = sensor_ps.sensors_battery()
        data.append(namedtuple_to_dict(battery, self.prefix, dict({'type': 'battery'})))
        return data

    def collect_data(self):
        data = []
        try:
            temperatures = self.get_temperatures()
            data.extend(temperatures)
        except AttributeError as ex:
            print 'Warn: do not support temperature sensor', ex

        try:
            fans = self.get_fans()
            data.extend(fans)
        except AttributeError as ex:
            print 'Warn: do not support fan sensor', ex

        try:
            battery = self.get_battery()
            data.extend(battery)
        except AttributeError as ex:
            print 'Warn: do not support battery sensor', ex

        return data

