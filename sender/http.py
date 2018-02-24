#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


class HttpSender:

    def __init__(self, url, gzip):
        self.url = url
        self.header = {}
        self.client = requests.Session()
        if gzip:
            self.header['Content-Type'] = 'application/gzip'
            self.header['Content-Encoding'] = 'gzip'
        else:
            self.header['Content-Type'] = 'application/json'
            self.header['Content-Encoding'] = 'json'

    def send(self, data_list):
        send_data = []
        for data in data_list:
            send_data.append(json.dumps(data))
        try:
            resp = self.client.post(url=self.url, headers=self.header, data='\n'.join(send_data))
            if resp.status_code is not 200:
                return resp.content
            return None
        except requests.exceptions.ConnectionError as ex:
            return ex




