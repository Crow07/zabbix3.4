# -*- coding:utf-8 -*-
import re
import json
import urllib2
from urllib2 import URLError
from zabbix_api_get_authid_project import Zabbix_Auth
from zabbix_api_get_templates_project import Zabbix_Get_Templates
from zabbix_api_get_groupids_project import Zabbix_Get_Groups

B = Zabbix_Get_Groups()
B.Group_Check_List()
GroupInfo = B.Group_Info()
i = []
for a in GroupInfo:
    i.append(int(a["groupid"]))
while 1:
    Input_Groupid = input("Please input groupid which you need: ")
    if Input_Groupid in i:
        print "group configuration done."
        break
    else:
        print "Input error,please try again."

C = Zabbix_Get_Templates()
C.Templates_Check_List()
TemplateInfo = C.Templates_Info()
m = []
for b in TemplateInfo:
    m.append(int(b["templateid"]))
while 1:
    Input_Templateid = input("Please input templateid which you need: ")
    if Input_Templateid in m:
        print "template configuration done."
        break
    else:
        print "Input error,please try again."

Authid = str(Zabbix_Auth().user_login())
f = open('E:/project/python/zabbix_api/ips')
for line in f.readlines():
    dic =re.split(r'[ ,\n]',line)
    hostname = dic[0]
    ip = dic[1]
    cpuinfo1 = dic[4]
    cpuinfo2 = dic[5]
    cpuinfo3 = dic[6]
    vender  = dic[7]
    model = dic[8]
    url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
    header = {"Content-Type": "application/json"}

    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": hostname,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                },
                {
                    "type": 2,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "161"
                }
            ],
            "groups": [
                {
                    "groupid": Input_Groupid
                }
            ],
            "templates": [
                {
                    "templateid": Input_Templateid
                }
            ],
            "inventory_mode": 0,
            "inventory": {
                "software_app_a": cpuinfo1,
                "software_app_b": cpuinfo2,
                "software_app_c": cpuinfo3,
                "vendor": vender,
                "model": model
            }
        },
        "auth": Authid,
        "id": 1
        })
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])
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
            hostsinfo = response['result']
            print hostsinfo