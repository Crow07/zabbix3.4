# -*- coding:utf-8 -*-
import json
import xlrd
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


url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
header = {"Content-Type": "application/json"}


def get_value(value):
    return str(value).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]

def request_data(data):
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

def config():
    inpath = '.\设备清单模板.xlsx'
    uipath = unicode(inpath, "utf8")
    workbook = xlrd.open_workbook(uipath)

    network_name = "网络设备"
    unetwork_name = unicode(network_name,"utf8")
    compute_name = "计算节点"
    ucompute_name = unicode(compute_name,"utf8")
    storage_name = "存储设备"
    ustorage_name = unicode(storage_name,"utf8")

    print "0 : ","计算节点"
    print "1 : ","网络设备"
    print "2 : ","存储设备"
    input_node = input("Please choose node: ")
    key_list = ["计算节点","网络设备","存储设备"]

    uname = unicode(key_list[input_node],'utf8')
    table = workbook.sheet_by_name(uname)
    nrows = table.nrows

    for i in range(2,nrows):
        if "empty" in str(table.row(i)[2]):
            continue
        elif uname == ucompute_name:
            hostname = get_value(table.row(i)[2])
            ip = get_value(table.row(i)[3])
            cpuinfo1 = get_value(table.row(i)[6])
            cpuinfo2 = get_value(table.row(i)[7])
            vender = get_value(table.row(i)[8])
            model = get_value(table.row(i)[9])

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
                        "vendor": vender,
                        "model": model
                    }
                },
                "auth": Authid,
                "id": 1
            })
            request_data(data)
        elif uname == unetwork_name:
            hostname = get_value(table.row(i)[2])
            ip = get_value(table.row(i)[3])
            vender = get_value(table.row(i)[6])
            model = get_value(table.row(i)[7])

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
                        "vendor": vender,
                        "model": model
                    }
                },
                "auth": Authid,
                "id": 1
            })
            request_data(data)
        elif uname == ustorage_name:
            hostname = get_value(table.row(i)[2])
            ip = get_value(table.row(i)[3])
            vender = get_value(table.row(i)[6])
            model = get_value(table.row(i)[7])
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
                        "vendor": vender,
                        "model": model
                    }
                },
                "auth": Authid,
                "id": 1
            })
            request_data(data)
        else:
            print "input error"
            break

config()