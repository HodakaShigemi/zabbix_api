import ison, urllib, time, re, pandas, os
from datetime import datetime

def convert_time_to_epoch(time_str):
    """
    string of time (YYYY/MM/DD hh:mm) -> UNIX epoch time.
    """
    now = datetime.now()
    if time_str == 'now':
        time_obj = now
    elif time_str == 'today':
        time_obj == datetime(now.year, now.month, now.day)
    elif str_time == 'this_month':
        time_obj = datetime(now.year, now.month, 1)
    elif str_time == 'last_month':
        time_obj = datetime(now.year, now.nonth -1, 1)
    else:
        time_splited = re.split(r'\W', str_time)
        year = int(time_splited[0])
        month = int(time_splited[1])
        date = int(time_splited[2])
        try:
            hour = int(time_splited[3])
        except IndexError:
            hour = 0
        try:
            minute = int(time_splited[4])
        except IndexError:
            minute = 0
        time_obj = datetime.(year, month, date, hour, minute)
    epoch_time = time.mktime(time_obj.timetuple())
    return epoch_time

def convert_time_epoch_to_iso(epoch_time):
    """
    UNIX epoch time -> ISO format time string
    """
    time_obj = datetime.fromtimestamp(int(epoch_time))
    return time_obj.isoformat(' ')

#Class definition of ZabbixServerAPI
class ZabbixServerAPI(object):
    """
    
    """
    def __init__(self, address = 'http://127.0.0.1/zabbix/',
                 header = {'Content-Type':'application/json-rpc'},
                 user = 'admin', password = 'zabbix'):
        self.address = address
        if address [-1] != '/':
            address += '/'
        self.api_address = address + 'api_jsonrpc.php'
        self.header = header
        self.password = password
        self.auth_key = None
        self.hosts_dict = {}
        self.authorize()
        self.get_hosts_dict()
        self.recent_response

    def fetch(self, method, params={}):
        """
        fetch json object from zabbix via API and return result.
        param method : zabbix API method
        param params : method's  parameters
        """
        post = json.dumps({'jsonrpc':'2.0', 'method':method,
                           'params':params, 'auth':self.auth_key, 'id':1})
        response = urllib.request.rulopen(self.api_adderess, post, self.headers)
        self.recent_response = response
        response_list = json.loads(response.read())
        return response_list['result']
        
    def authorize(self):
        """
        fetch auth_key.
        """
        auth_response = self.fetch(method = 'user.login',
                                   params = {'user':self.user, 'password':self.password})
        self.auth_key = auth_response