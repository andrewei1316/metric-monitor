#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import rfc3339
from metrics.cpu import CpuInfo
from metrics.disk import DiskInfo
from metrics.net import NetworkInfo
from metrics.sensor import SensorInfo
from metrics.memory import MemoryInfo
from metrics.system import SystemInfo

from sender.http import HttpSender


def collect():
    data = []
    cpu = CpuInfo()
    cpu_data = cpu.collect_data()
    # print 'cpu_data =', cpu_data
    data.extend(cpu_data)

    mem = MemoryInfo()
    mem_data = mem.collect_data()
    # print 'mem_data =', mem_data
    data.extend(mem_data)

    disk = DiskInfo()
    disk_data = disk.collect_data()
    # print 'disk_data =', disk_data
    data.extend(disk_data)

    net = NetworkInfo()
    net_data = net.collect_data()
    # print 'net_data =', net_data
    data.extend(net_data)

    sensor = SensorInfo()
    sensor_data = sensor.collect_data()
    # print 'sensor_data =', sensor_data
    data.extend(sensor_data)

    system = SystemInfo()
    system_data = system.collect_data()
    # print 'system_data =', system_data
    data.extend(system_data)

    sender_data = []
    hostname = socket.gethostname()
    timestamp = rfc3339.rfc3339(time.time(), utc=True, use_system_timezone=False)
    for d in data:
        d['hostname'] = hostname
        d['timestamp'] = timestamp
        sender_data.append(d)
    return sender_data


def main():
    http_sender = HttpSender('http://127.0.0.1:4000/logkit/data', False)
    while True:
        sender_data = collect()
        resp = http_sender.send(sender_data)
        if resp:
            print resp
        time.sleep(3)


if __name__ == '__main__':
    main()

