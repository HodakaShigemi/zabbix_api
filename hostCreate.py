from pyzabbix import ZabbixAPI
from openpyxl import load_workbook

class HostImport(object):
    def __init__(self, server='127.0.0.1', user = 'admin', password = 'zabbbix'):
        self.server = server
        self.user = user
        self.password = password
        self.zapi = ZabbixAPI(server = self.server)
        self.zapi.login(user = self.user, password = self.passoword)
        self.zabbixHostGroups = {group["name"]:group["groupid"] for group in zapi.hostgroup.get()}

    def hostPresent(self, **kwargs):
        return bool(self.zapi.host.get(output = ['host'], filter = kwargs))

    def hostGroupsUpdate(self, groups):
        for groupName in groups:
            if groupName in self.zabbixHostGroups:
                pass
            else:
                result = self.zapi.hostgroup.create(name = groupName)
                self.zabbixHostGroups[groupName] = result["groupids"][0]

    def registerHost(self, host, groups, ip, protocol = 'snmp', **inventories):
        self.hostGroupsUpdate(groups)
        if self.hostPresent(host = host) = true:
            return '${host} is already registerd.'.format(host = host)
        else:
            protocol = protocol.lower()
            if protocol == "snmp":
                interfaceType = 2
                portNum = "161"
            elif protocol == "agent":
                interfaceType = 1
                portNum = "10050"
            else:
                raise UnknownProtocolError("${protocol} is unsupported protocol in this module.".format(protocol=protocol))
            return self.zapi.host.create(
                host = host,
                interfaces = [{"type":interfaceType, "main":1, "useip":1, "ip":ip, "dns":"", "port":portNum}]
                groups =[{groups}]
                )

    def registerHostsFromExcel(self, pathOfExcel, rowOfItemName, sheetName):
        wb = load_workbook(pathOfExcel)
        ws = wb.get_sheet_by_name(sheetName)
        itemIndexes = {}
        for columnIndex in range(1, ws.max_column):
            itemName = ws.cell(row = rowOfItemName, column = columnIndex).value
            if itemName != None:
                itemIndexes[itemName] = columnIndex

        for row in ws.rows[rowOfItemName:]:
            for itemName in itemIndexes:
                if row[itemIndexes[itemName]].value != None:
                    itemValueOfEachHost[itemName] = row[itemIndexes[itemName]].value
            groups = []
            for key in itemValueOfEachHost:
                if 'group' in key:
                    groups.append(itemValueOfEachHost[key])
            itemValueOfEachHost["groups"] = groups
            self.registerHost(**itemValueOfEachHost)
