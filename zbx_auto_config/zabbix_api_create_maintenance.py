# -*- coding:utf-8 -*-
import re
import json
import urllib2
from urllib2 import URLError
from zabbix_api_get_authid_project import Zabbix_Auth
from zabbix_api_get_groupids_project import Zabbix_Get_Groups

Authid = str(Zabbix_Auth().user_login())

P = Zabbix_Get_Groups()
P.Group_Check_List()
GroupInfo = P.Group_Info()

m = []
for b in GroupInfo:
    m.append(int(b["groupid"]))
while 1:
    Input_Groupid = input("Please input groupid which you will use: ")
    if Input_Groupid in m:
        print "group selected."
        break
    else:
        print "Input error,please try again."


class Zabbix_create_maintenance:
    def __init__(self):
        self.url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
        self.header = {"Content-Type": "application/json"}

    def create_maintenance(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "maintenance.create",
            "params": {
                "name": "test maintenance",
                "active_since": 1358844540,
                "active_till": 1390466940,
                "groupids": [
                    Input_Groupid
                ],
                "timeperiods": [
                    {
                        "timeperiod_type": 3,
                        "every": 1,
                        "dayofweek": 64,
                        "start_time": 64800,
                        "period": 3600
                    }
                ]
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
            if "error" in response:
                print response["error"]["data"]
            else:
                self.maintenanceinfo = response['result']
                return self.maintenanceinfo

A = Zabbix_create_maintenance()
print A.create_maintenance()