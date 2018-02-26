#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gzip
import requests
import StringIO
import ConfigParser
from base import Sender
from tools.models import *


class HttpSender(Sender):
    by_zip = True
    url = 'http://127.0.0.1'

    def __init__(self, conf):
        Sender.__init__(self)
        if not conf:
            return
        try:
            url = conf.get(SENDER_HTTP, SENDER_HTTP_URL)
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass
        else:
            self.url = url
        try:
            by_gzip = conf.get(SENDER_HTTP, SENDER_HTTP_GZIP)
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass
        else:
            self.by_gzip = by_gzip

        self.header = {}
        self.client = requests.Session()
        if self.by_gzip:
            self.header['Content-Type'] = 'application/gzip'
            self.header['Content-Encoding'] = 'gzip'
        else:
            self.header['Content-Type'] = 'application/json'
            self.header['Content-Encoding'] = 'json'

    def gzip_data(self, send_data):
        s = StringIO.StringIO()
        g = gzip.GzipFile(fileobj=s, mode='w')
        g.write(send_data)
        g.close()
        return s.getvalue()

    def send(self, data_list):
        send_data = []
        for data in data_list:
            send_data.append(json.dumps(data))
        send_data = '\n'.join(send_data)
        if self.by_gzip:
            send_data = self.gzip_data(send_data)
        try:
            resp = self.client.post(url=self.url, headers=self.header, data=send_data)
            if resp.status_code is not 200:
                print 'Error: send data error:', resp.content
        except requests.exceptions.ConnectionError as ex:
            print 'Error: send data error:', ex




