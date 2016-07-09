#!/bin/bash

zabbixPath=`ls -d /usr/share/doc/* | grep -e"zabbix-server-mysql-.*"`
/usr/bin/mysql -uroot zabbix < ${zabbixPath}/create/schema.sql
/usr/bin/mysql -uroot zabbix < ${zabbixPath}/create/images.sql
/usr/bin/mysql -uroot zabbix < ${zabbixPath}/create/data.sql
