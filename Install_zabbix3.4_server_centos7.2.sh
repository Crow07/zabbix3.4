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
mv /etc/yum.repos.d/* /etc/yum.repos.d.bak/
cp -rf /home/conf/CentOS-local.repo /etc/yum.repos.d/
yum clean all


#install zbx server 
yum -y install zabbix-server-mysql zabbix-web-mysql zabbix-agent
#install zbx mariadb-server 
yum -y install mariadb mariadb-server
#install snmp-utils
yum install -y net-snmp net-snmp-utils net-tools


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

mysql -e "create database zabbix character set utf8 collate utf8_bin;"
mysql -e "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"
cd /usr/share/doc/zabbix-server-mysql-3.4.1
zcat create.sql.gz | mysql zabbix

#httpd config

sed -i "/php_value date.timezone/s/^.*$/\tphp_value date.timezone Asia\/Shanghai/g" /etc/httpd/conf.d/zabbix.conf
sed -i "/php_value memory_limit/s/^.*$/\tphp_value memory_limit 512M/g" /etc/httpd/conf.d/zabbix.conf

#zabbix config
[ ! -f /etc/zabbix/zabbix_server.conf.bak ] && mv /etc/zabbix/zabbix_server.conf /etc/zabbix/zabbix_server.conf.bak
cp -rf /home/conf/zabbix_server.conf /etc/zabbix/zabbix_server.conf

start_service_enable "zabbix-server"
start_service_enable "httpd"
start_service_enable "mariadb"
start_service_enable "snmpd"




