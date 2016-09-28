#!/bin/bash

zabbixPath=`ls -d /usr/share/doc/* | grep -e"zabbix-server-mysql-.*"`
/usr/bin/mysql -uroot --password=password zabbix < ${zabbixPath}/create/schema.sql
/usr/bin/mysql -uroot --password=password zabbix < ${zabbixPath}/create/images.sql
/usr/bin/mysql -uroot --password=password zabbix < ${zabbixPath}/create/data.sql
