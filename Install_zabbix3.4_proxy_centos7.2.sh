#!/bin/bash
##init system


function print()
{
   echo -e "\033[40;36m[`date +%Y-%m-%d\ %H:%M:%S`] [info] $1 \033[0m" 
   return 0
}

function start_service_enable()
{
    service=$1
	
    print "start and chkconfig on: ${service}" 
    systemctl restart ${service} 
    systemctl enable ${service} 	
    return 0
}

function start_service_disable()
{
    service=$1
	
    print "stop and chkconfig off: ${service}" 
    systemctl stop ${service} 
    systemctl disable ${service} 	
    return 0
}

#make yum
mkdir -p /etc/yum.repos.d.bak
mv /etc/yum.repos.d/* /etc/yum.repos.d.bak/
cp -rf ./conf/CentOS-local.repo /etc/yum.repos.d/
yum clean all


#install zbx server 
yum -y install zabbix-proxy
#install zbx mariadb-server 
yum -y install mariadb mariadb-server
#install snmp-utils
yum install -y net-snmp net-snmp-utils
yum install -y net-tools

## close selinux
print "selinux already closed"
setenforce 0
sed -i "/SELINUX=enforcing/s/^.*$/SELINUX=disabled/g" /etc/selinux/config

##close firewall
start_service_disable "firewalld"


##change defult open file
ulimit -HSn 65535
if ! egrep '^\*' /etc/security/limits.conf
then
	echo -e '* - nofile  65535' >> /etc/security/limits.conf
	echo -e 'root - nofile 100000' >> /etc/security/limits.conf
fi
print "open file has configured"


##set timezone for centos7
timedatectl set-timezone Asia/Shanghai
print "timezone has configured"

#install mysql
mysql_install_db
chmod -R 777 /var/lib/mysql

##mysql config
[ ! -f /etc/my.cnf.bak ] && mv /etc/my.cnf /etc/my.cnf.bak
cp -rf /home/conf/my.cnf /etc/my.cnf

mkdir -p /home/mysql && chown -R mysql.mysql /home/mysql/

systemctl start mariadb

mysql -e "create database zabbix_proxy character set utf8 collate utf8_bin;"
mysql -e "grant all privileges on zabbix_proxy.* to zabbix@localhost identified by 'zabbix';"
cd /usr/share/doc/zabbix-proxy-mysql-3.4.1
zcat schema.sql.gz| mysql zabbix_proxy

#zabbix config
[ ! -f /etc/zabbix/zabbix_proxy.conf.bak ] && mv /etc/zabbix/zabbix_proxy.conf /etc/zabbix/zabbix_proxy.conf.bak
cp -rf /home/conf/zabbix_proxy.conf /etc/zabbix/zabbix_proxy.conf

start_service_enable "zabbix-proxy"
start_service_enable "mariadb"
start_service_enable "snmpd"


