#!/bin/bash

zabbixPath=`ls -d /usr/share/doc/* | grep -e"zabbix-server-mysql-.*"`
eval /usr/bin/mysql/ -uroot zabbix < ${zabbixPath}/create/schema.sql
eval /usr/bin/mysql/ -uroot zabbix < ${zabbixPath}/create/images.sql
eval /usr/bin/mysql/ -uroot zabbix < ${zabbixPath}/create/data.sql
