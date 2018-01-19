# -*- coding:utf-8 -*-

import json
import urllib2
from urllib2 import URLError


class Zabbix_Auth:
    def __init__(self):
        self.url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
        self.header = {"Content-Type": "application/json"}

    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "Admin",
                "password": "zabbix"
            },
            "id": 0
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m authenticate is failed, please check it !\033[0m", e.code
        else:
            response = json.loads(result.read())
            result.close()
            self.authID = response['result']
            return self.authID