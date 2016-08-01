import json, urllib2, datetime, time, re, pandas, os, sys

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
    elif str_time == 'last_month':
         hoge_time = datetime.datetime(now.year, now.month -1, 1)
    elif str_time == 'this_month':
         hoge_time = datetime.datetime(now.year, now.month, 1) 
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
    """This class is defined to access to zabbix server API,
        to get informations vi athe API."""
    def __init__(self, address = 'http://172.31.254.6/zabbix/',
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
        """Assume method as string of zabbix api method,and params as dictionary of patameters.
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
            self.hosts_dict[elm['hostid']] = elm['name']

    def host_attr(self, host_id, host_attr=''):
        """It returns attributes of a host.
           The host is identified by host_id.
           You can spedcify attribute by host_attr."""
        host_get_list = self.fetch('host.get', params={'hostids':host_id})
        if host_attr != '':
            return host_get_list[0][host_attr]
        else:
            return host_get_list[0]

    def get_graph_id_dict(self, host_ids):
        """Assume host_ids as host id stirng or list.
           It returns dictionary whose keys are graphs' names """
        graph_get_list = self.fetch(method = 'graph.get', 
                                    params = {'hostids':str(host_ids)})
        graphs_dict = {}
        for elm in graph_get_list:
            graphs_dict[elm['name']] = elm['graphid']
        return graphs_dict

    def save_graph_image(self, graph_id, time_from = '', time_till = '', width = '1900', height = '600', border ='0', save_as = 'fuga.jpg'):
        """Assume graph_id as string of graph id, time_from and time_till as string of time YYYY/MM/DD.
           It saves graph image of graph_id."""
        if time_from == '':
            time_from = 'last_month'
            start_time = datetime.datetime
        if time_till == '':
            time_till = 'this_month'
        time_from = str_to_epoch(time_from)
        time_till = str_to_epoch(time_till)
        period = str(int(time_till - time_from))
        time_from = epoch_to_iso(time_from)
        stime = time_from.translate(None, '- :')
        opener = urllib2.build_opener()
        opener.addheaders.append(("cookie", "zbx_sessionid=" + self.auth_key))
        graph_url = self.address + "chart2.php" 
        graph_get_url = "%s?graphid=%s&width=%s&height=%s&border=%s&period=%s&stime=%s" % (graph_url,
                         graph_id, width, height, border, period, stime)
        graph = opener.open(graph_get_url)
        graph_file = open('fuga.jpg', 'w')
        graph_file.write(graph.read())
        graph_file.close()

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
            item_dict[items[key]['itemid']] = key 
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

    def save_history_of_item(self, item_id, time_from='', time_till='', save_as = 'hoge.csv'):
        """Assume save_as as string of path and name where file is saved,
           time_from and time_till as string of time YYYY/MM/DD.
           It save history (time_from ~ time_till) of item as csv file."""
        item_info = self.item_attr(item_id)
        host_info = self.host_attr(item_info['hostid'])
        info = {}
        info['host_ip'] = host_info['host']
        info['description'] = host_info['description']
        info['item_name'] = item_info['name']
        info['unit'] = item_info['units']
        host_name = host_info['host']
        host_name = host_name.replace('/','')
        key = item_info['key_']
        info_pandas = pandas.DataFrame([info])
        info_pandas.to_csv(save_as)
        history_of_item = self.get_history_of_item(item_id, time_from, time_till)
        time_stamp = history_of_item[0]['clock'].translate(None, ' -:')
        time_stamp = time_stamp +'-'+ history_of_item[-1]['clock'].translate(None, ' -:')
        history_pandas = pandas.DataFrame(history_of_item)
        history_pandas[['clock', 'value']].to_csv(save_as, mode = 'a')
        rename = time_stamp + key + host_name + '.csv'
        return save_as, rename

args = sys.argv
if args[1]:
    zbx = ZabbixServer(address = args[1])
else:
    zbx = ZabbixServer()

import bottle, wtforms

class HistForm(wtforms.form.Form):
    host_id = wtforms.fields.SelectField(label=u'Select Host',coerce = str)
    items_id = wtforms.fields.SelectField(u'Item ID', coerce = str)
    from_time = wtforms.StringField(label='Time from')
    to_time = wtforms.StringField(label='Time to')
    save = wtforms.fields.SubmitField('save')
"""    def iter_choices(self):
        current_value = self.data if sele.data is not None else self.coerce(sel.default)
        for value, vabel in self.choices:
            yield (value, vabel, self.coerce(value) == current_value)"""

form = HistForm()

def show_hosts():
     hosts = zbx.hosts_dict
     return [("-","-")] + [(key, hosts[key]) for key in hosts]

def show_items(id):
    items = zbx.get_items_dict(id)
    return [(key, items[key]) for key in items]

@bottle.get('/history')
def index(hostid = '', itemid = ''):
    form = HistForm()
    return bottle.template('index', hostid = hostid, itemid = itemid)

@bottle.get('/save')
def ask_host():
    #get parameters
    hosts = show_hosts()
    return bottle.template('save.tpl', form = form, hosts = hosts, host_id = "-")
@bottle.post('/save')
def save():
    if bottle.request.forms.host_id:
        print bottle.request.forms.decode()
        # form.iter_choices(), 
        hosts = show_hosts()
        host_id = bottle.request.forms.host_id.decode()
        form.host_id.choices = hosts
        form.items_id.choices = show_items(host_id)
        return bottle.template('save.tpl', form = form, hosts = hosts, host_id = host_id)
    elif bottle.request.forms.items_id:
        hosts = show_hosts()
        host_id = bottle.request.forms.host_id.decode()
        item_id = bottle.request.forms.items_id.decode()
        print item_id
        from_time = bottle.request.forms.from_time
        to_time = bottle.request.forms.to_time
        save_as, rename = zbx.save_history_of_item(item_id, from_time, to_time)
        # return bottle.template('save.tpl', form = form, hosts = hosts, host_id = host_id)
        return bottle.static_file(save_as, root = './', download = rename)
    else:
        return bottle.template('save.tpl', form = form)

@bottle.get('/graph')
def send_graph():
    return bottle.static_file('fuga.jpg', root = './')

#start built in server
if __name__ == '__main__':
    bottle.run(host = '0.0.0.0', port = 8080, debug = True, reloader = True)

