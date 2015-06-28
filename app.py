import json, urllib2, datetime, time, pandas

def str_to_epoch(str_time):
    """Assume str_time as string of time YYYY/MM/DD or now.
       It returns a integer of Unix Epoch time of YYYY/MM/DD/00:00"""
    now = datetime.datetime.now()
    if str_time == 'now':
         hoge_time = now
    elif str_time == 'today':
         hoge_time = datetime.datetime(now.year, now.month, now.day)
    elif str_time == 'on_the_hour':
         hoge_time = datetime.datetime(now.year, now.month, now.day, now.hour)
    else:
        print str_time
        time_splited = str_time.split(',')
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
        hoge_time = datetime.datetime(year, month, date, hour, minute)
    epoch_time = time.mktime(hoge_time.timetuple())
    return epoch_time

def epoch_to_iso(epoch_time):
    """Assume epoch_time as Unix Epoch Time.
       It converts epoch_time to string of  ISO format time."""
    date_obj = datetime.datetime.fromtimestamp(int(epoch_time))
    return date_obj.isoformat(' ')



#class difinition of ZabbixServer
class ZabbixServer(object):
    """This class is defined to access to zabbix server API."""
    def __init__(self, address = 'http://192.168.56.102/zabbix/',
                 header = {'Content-Type':'application/json-rpc'},
                 user = 'admin', password = 'zabbix'):
        self.address = address
        if address[-1] != '/':
            address += '/'
        self.api_address = address + 'api_jsonrpc.php'
        self.headers = header
        self.user = user
        self.password = password
        self.auth_key = None
        self.hosts_dict = {}
        self.authorize()
        self.get_hosts_dict()
        self.recent_response

    def fetch(self, method, params={}):
        """Assume method as string of zabbix api method.
           It returns a list which contains dictionaries of responses from zabbix api."""
        post = json.dumps({'jsonrpc':'2.0', 'method':method,
                                'params':params, 'auth':self.auth_key, 'id':1})
        request = urllib2.Request(self.api_address, post, self.headers)
        response = urllib2.urlopen(request)
        response_str = response.read()
        response_list = json.loads(response_str)
        self.recent_response = response_list
        return response_list['result']

    def authorize(self):
        """It gets authentification key from zabbix server.
           The authentification key is saved in self.auth_key"""
        auth_response = self.fetch(method = 'user.login',
                            params = {'user':self.user, 'password':self.password})
        self.auth_key = auth_response

    def get_hosts_dict(self):
        """It gets a dictionary whose keys are host names and
           values are host IDs the zabbix server is watching.
           The dictionary is saved in self.hosts_dict."""
        host_get_list = self.fetch(method = 'host.get')
        for elm in host_get_list:
            self.hosts_dict[elm['name']] = elm['hostid']

    def host_attr(self, host_id, host_attr=''):
        host_get_list = self.fetch('host.get', params={'hostids':host_id})
        if host_attr != '':
            return host_get_list[0][host_attr]
        else:
            return host_get_list[0]

    def get_items_of_host(self, host_ids):
        """Assume host_ids as host id stirng or list.
           It returns dictionary whose keys are item keys, and values are item IDs."""
        item_get_list = self.fetch(method = 'item.get',
                                   params = {'hostids':str(host_ids)})
        items_dict = {}
        for elm in item_get_list:
            items_dict[elm['key_']] = {'itemid': elm['itemid'],
                                       'lastvalue':elm['lastvalue'],
                                       'units':elm['units']}
        return items_dict

    def get_items_dict(self, host_id):
        items = self.get_items_of_host(host_id)
        item_dict = {}
        for key in items:
            item_dict[key] = items[key]['itemid']
        return item_dict

    def item_attr(self, item_id, item_attr = ''):
        """Assume item_id as stirng of item ID, item_attr as string of item's attirbute.
           It returns the item's attribute which is indicated by item_attr.
           It returns all attributes of the item,if item_attr is empty"""

        item_get_list = self.fetch('item.get', params={'itemids':item_id})
        if item_attr != '':
            return item_get_list[0][item_attr]
        else:
            return item_get_list[0]

    def get_history_of_item(self, item_id, time_from = '', time_till = ''):
        """Assume item_id as zabbix api item's ID, time_from as string of time
           (yyyy,mm,dd,hh,mm).
           It reuturns a list whose elements are dictionary of item's history"""
        if time_from == '':
            time_from ='on_the_hour'
        if time_till == '':
            time_till = 'now'
        epoch_time_from = str_to_epoch(time_from)
        epoch_time_till = str_to_epoch(time_till)
        history_get_list = self.fetch(method = 'history.get',
                                      params = {'history':self.item_attr(item_id,'value_type'),
                                                'itemids' : item_id,
                                                'time_from':epoch_time_from,
                                                'time_till':epoch_time_till})
        for dict in history_get_list:
            dict['clock'] = epoch_to_iso(dict['clock'])
        return history_get_list

    def save_history_of_item(self, item_id, save_as = 'hoge.csv', time_from='', time_till=''):
        """Assume save_as as string of path and name where file is saved,
           time_from and time_till as string of time YYYY/MM/DD.
           It save history (time_from ~ time_till) of item as csv file."""
        item_info = self.item_attr(item_id)
        host_info = self.host_attr(item_info['hostid'])
        info = {}
        info['host_name'] = host_info['name']
        info['description'] = host_info['description']
        info['item_name'] = item_info['name']
        info['unit'] = item_info['units']
        info_pandas = pandas.DataFrame([info])
        info_pandas.to_csv(save_as)
        history_of_item = self.get_history_of_item(item_id, time_from, time_till)
        history_pandas = pandas.DataFrame(history_of_item)
        history_pandas[['clock', 'value']].to_csv(save_as, mode = 'a')



import bottle

zbx = ZabbixServer()

@bottle.route('/hello')
def hello():
	#describe tmplate
	return bottle.template('Hello {{string}}', string = 'world')

@bottle.post('/form')
def form():
	#get parameters
	id = bottle.request.forms.get('id')
	return bottle.template('id = {{id}}', id = id)

@bottle.route('/hoge')
def hoge():
    hogehoge = fetch()
    return bottle.template(hogehoge)

@bottle.route('/zabi')
def zabi():
    host_dict = zbx.hosts_dict
    host_list = []
    for key in host_dict:
        host_list.append(key)
        host_list.append(host_dict[key])
    return host_dict

@bottle.route('/itemofhost/<id>')
def itemofhost(id):
    hostid = id
    items = zbx.get_items_dict(hostid)
    return items

@bottle.route('/itemattr/<hostid>/<itemid>')
def itemattr(hostid, itemid):
    itemid = itemid  
    return zbx.item_attr(itemid)

#start built in server
if __name__ == '__main__':
	bottle.run(host = 'localhost', port = 8080, debug = True, reloader = True)
