# -*- coding:utf-8 -*-

import json
import urllib2
from urllib2 import URLError
from zabbix_api_get_authid_project import Zabbix_Auth

Authid = str(Zabbix_Auth().user_login())

class Zabbix_Get_Templates:
    def __init__(self):
        self.url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
        self.header = {"Content-Type": "application/json"}

    def Templates_Info(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend"
            },
            "auth": Authid,
            "id": 1
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
            self.templateinfo = response['result']
            return self.templateinfo
    def Templates_Check_List(self):
        A =  Zabbix_Get_Templates()
        print "----Template List----"
        print "ID: ","TemplateName"
        print "--", "  ----------"
        for i in A.Templates_Info():
            print i["templateid"],":",i["name"]
        print "----Template List----"