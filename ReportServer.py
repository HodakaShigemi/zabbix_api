from pyzabbix import ZabbixAPI
from datetime import datetime
import re, time, pandas

class GenerateReport(object):
    """
    ZabbixAPIを使用して各種のデータを収集整形する
    """

    def __init__(self, server = "http://127.0.0.1/zabbix"):
        """
        初期設定を行う
        デフォルトでサーバのURLはローカルのzabbixサーバになっている
        """
        self.zapi = ZabbixAPI(server = server)
        self.hosts_dictionary = {}

    def update_hosts_dictionary(self):
        """
        ホストの辞書データを更新する
        辞書は self.hosts_dictionary = {"ホスト":"ホストのID", ...}となっている
        """
        for host in self.zapi.host.get(output=["host"]):
            self.hosts_dictionary[host["host"]] = host["hostid"]

    def items_dictionary_of_host(self, hostid):
        """
        特定のホストに属するアイテムの辞書を得る
        この関数はホストのhostidを必要とする
        辞書は {"アイテムのkey":"アイテムID",....}となっている
        """
        items_list = self.zapi.item.get(hostids=hostid, output=["key_"])
        items_dictionary_of_host = {}
        for item in items_list:
            items_dictionary_of_host[item["key_"]] = item["itemid"]
        return items_dictionary_of_host

    def attribute_of_host(self, hostid):
        return self.zapi.host.get(hostids = hostid)[0]

    def string_to_Unix_time(self, time_string):
        """
        文字列表現の時間をUNIX時間に変換する
        """
        now = datetime.now()
        if time_string == 'last_month':
            time = datetime(now.year, now.month -1, 1)
        elif time_string == 'this_month':
            time = datetime(now.year, now.month, 1)
        else:
            time_splited = re.split(r'¥W', time_string)
            for i in range(len(time_splited)):
                time_splited[i] = int(time_splited[i])
            while len(time_splited) < 3:
                time_splited.append(1)
            time = datetime(*time_splited)
        Unix_time = int(time.timestamp())
        return Unix_time

    def Unix_time_to_string(self, Unix_time):
        return datetime.fromtimestamp(int(Unix_time)).isoformat(' ')

    def history_of_item(self, itemid, time_from, time_till):
        time_from = self.string_to_Unix_time(time_from)
        time_till = self.string_to_Unix_time(time_till)
        return self.zapi.history.get(itemids =itemid, time_from = time_from, time_till = time_till)

    def save_history_as_csv(self, itemid, time_from, time_till, name_saving_file = "hoge.csv"):
        """
        特定のアイテムのヒストリーをcsvファイルに保存する。
        ヒストリの時間はUNIXタイムスタンプからISOフォーマットに変換する。
        """
        history_of_item = self.history_of_item(itemid = itemid, time_from = time_from, time_till = time_till)
        for row in history_of_item:
            row['clock'] = Unix_time_to_string(row['clock'])
        history_dataframe = pandas.DataFrame(history_of_item)
        history_dataframe['clock', 'value'].to_csv(name_saving_file, mode = 'a')


class Server(object):
    """
    
    """
