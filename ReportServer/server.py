from wtforms.form import Form
from wtforms.fields import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms import widgets
from bottle import get, post, redirect, run, template, request, static_file
from makeReport import ZabbixReportAPI
from tempfile import TemporaryDirectory
from tqdm import tqdm
from datetime import datetime
import zipfile, re

#class CheckedCheckboxInput(widgets.CheckboxInput):

class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    #option_widget = widgets.html_params(checked=True)

class ItemHistoryForm(Form):
    host_name = SelectField('Host Name')
    item = SelectField('Item', coerce = str)
    time_from = StringField('Time from')
    time_till = StringField('Time till')
    submit = SubmitField('Download CSV')

class ReportForm(Form):
    screen = MultiCheckBoxField('Screens')
    time_from = StringField('Time from')
    time_till = StringField('Time till')
    submit = SubmitField('Download ZIP')

#zabbix = ZabbixReportAPI(server='http://172.31.254.6/zabbix')
zabbix = ZabbixReportAPI()
report_template = '/root/zabbix_api/templateSI5.docx'

@get('/')
def redirect_to_top():
    redirect('/top')

@get('/top')
def top():
    title = 'トップ画面'
    return template('top', title=title, request=request)

@get('/history')
def history():
    title = 'アイテムのヒストリから値一覧を取得'
    zabbix.update_hosts_dictionary()
    host_names = list(zabbix.hosts_dictionary.keys())
    host_names.sort()
    item_history_form = ItemHistoryForm()
    return template(
        'history',
        title = title,
        request = request,
        item_history_form = item_history_form,
        host_names = host_names,
        selected_host = None
    )

@post('/history')
def save_history():
    title='save history'
    item_history_form = ItemHistoryForm(request.forms.decode())
    if item_history_form.host_name.data != 'None':
        selected_host = item_history_form.host_name.data
        host_id = zabbix.hosts_dictionary[selected_host]
        host_names = list(zabbix.hosts_dictionary.keys())
        host_names.sort()
        items_dictionary = zabbix.items_dictionary_of_host(host_id)
        items = list(items_dictionary.keys())
        items.sort()
        item_history_form.item.choices = list((items_dictionary[item], item) for item in items)
        now = datetime.now()
        last_month = datetime(now.year, now.month -1, 1).isoformat().replace('T', ' ')
        this_month = datetime(now.year, now.month, 1).isoformat().replace('T', ' ')
        return template(
            'history',
            title = title,
            request = request,
            selected_host = selected_host,
            host_names = host_names,
            item_history_form = item_history_form,
            last_month = last_month,
            this_month = this_month
        )
    elif item_history_form.item.data != 'None':
        tmp_dir = TemporaryDirectory(prefix = 'history')
        saved_path = zabbix.save_history_as_csv(
            itemid = item_history_form.item.data,
            time_from = item_history_form.time_from.data,
            time_till = item_history_form.time_till.data,
            save_as = tmp_dir.name + '/history.csv'
        )
    return static_file(saved_path, root='/', download = 'history.csv')
    
@get('/report')
def report():
    title = 'レポートを.docxファイルで保存'
    zabbix.update_screens_dictionary()
    screens = list(zabbix.screens_dictionary.keys())
    report_form = ReportForm()
    screens =  list(zabbix.screens_dictionary.keys())
    screens.sort()
    report_form.screen.choices = list((screen, screen) for screen in screens)
    now = datetime.now()
    last_month = datetime(now.year, now.month -1, 1).isoformat().replace('T', ' ')
    this_month = datetime(now.year, now.month, 1).isoformat().replace('T', ' ')
    return template(
        'report.tpl',
        title = title,
        request = request,
        report_form = report_form,
        last_month = last_month,
        this_month = this_month
    ) 

@post('/report')
def save_report():
    forms = request.forms.decode()
    if forms.screen:
        tmp_dir = TemporaryDirectory(prefix = 'report')
        zip_file = zipfile.ZipFile(tmp_dir.name + '/reports.zip', 'w', zipfile.ZIP_DEFLATED)
        regexp_sinetdc = re.compile(r'[0-9]{2}(.).+DC.*')
        for screen in tqdm(forms.getall('screen')):
            if '共同調達' in screen:
                dc_name = regexp_sinetdc.search(screen).group().replace('DC', '')
                file_name = dc_name + '.docx'
            else:
                file_name = screen.replace(' ', '').replace('　', '') + '.docx'

            screenid = zabbix.screens_dictionary[screen]
            time_from = forms.time_from
            time_till = forms.time_till
            report_file_path = zabbix.save_report_from_screen(screenid = screenid,
                                                              time_from = time_from,
                                                              time_till = time_till,
                                                              template = report_template,
                                                              save_as = tmp_dir.name + '/' + file_name)
            zip_file.write(report_file_path)
        zip_file.close()
        return static_file(zip_file.filename, root ='/', download = 'reports.zip')

    else:
        print('no screens selected')
        for screen in forms.getall('screen'):
            print(screen)
        return template('top', request = request, title = 'hoge')
        print('hoge')

if __name__=='__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
