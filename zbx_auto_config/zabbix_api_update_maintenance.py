# -*- coding:utf-8 -*-
import re
import json
import urllib2
from urllib2 import URLError
from zabbix_api_get_authid_project import Zabbix_Auth
from zabbix_api_get_maintenance import Zabbix_Get_Maintenance

Authid = str(Zabbix_Auth().user_login())

P = Zabbix_Get_Maintenance()
P.Maintenance_Check_List()
MaintenanceInfo = P.Maintenance_Info()

m = []
for b in MaintenanceInfo:
    m.append(int(b["maintenanceid"]))
while 1:
    Input_Maintenanceid = input("Please input maintenanceid which you will update: ")
    if Input_Maintenanceid in m:
        print "maintenanceid selected."
        break
    else:
        print "Input error,please try again."

class Zabbix_update_maintenance:
    def __init__(self):
        self.url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
        self.header = {"Content-Type": "application/json"}

    def update_maintenance(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "maintenance.update",
            "params": {
                "maintenanceid": Input_Maintenanceid,
                "active_since": 1515513600,
                "active_till": 1518192000,
                "timeperiods": [
                    {
                        "timeperiod_type": 3,
                        "every": 1,
                        "dayofweek": 64,
                        "start_time": 64800,
                        "period": 3600
                    }
                ],
                "groupids": [
                    "2"
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
                self.updateinfo = response['result']
                return self.updateinfo

    def delete_maintenance(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "maintenance.delete",
            "params": [
                Input_Maintenanceid
            ],
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
                self.deleteinfo = response['result']
                return self.deleteinfo

A = Zabbix_update_maintenance()
print A.update_maintenance()
print A.delete_maintenance()