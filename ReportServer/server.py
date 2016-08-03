from wtforms.form import Form
from wtforms.fields import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms import widgets
from bottle import get, post, redirect, run, template, request, static_file
from makeReport import ZabbixReportAPI 

class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ItemHistoryForm(Form):
    host_name = SelectField('Host Name')
    item = SelectField('Item', coerce = str)
    time_from = StringField('Time from')
    time_till = StringField('Time till')
    submit = SubmitField('Download CSV')

class ReportForm(Form):
    screen = MultiCheckBoxField('Screens', render_kw={'type':'checkbox'})
    time_from = StringField('Time from')
    time_till = StringField('Time till')
    submit = SubmitField('Download ZIP')

zabbix = ZabbixReportAPI()

@get('/')
def redirect_to_top():
    redirect('/top')

@get('/top')
def top():
    title = 'トップ画面'
    return template('top', title=title, request=request)

@get('/history')
def history():
    title='アイテムのヒストリから値一覧を取得'
    zabbix.update_hosts_dictionary()
    host_names = list(zabbix.hosts_dictionary.keys())
    host_names.sort()
    item_history_form = ItemHistoryForm()
    return template(
        'history',
        title=title,
        request=request,
        item_history_form=item_history_form,
        host_names=host_names,
        selected_host=None
    )

@post('/history')
def save_history():
    title='hoge'
    item_history_form = request.forms
    if item_history_form.host_name:
        host_names = list(zabbix.hosts_dictionary.keys())
        host_names.sort()
        item_history_form = 
    

if __name__=='__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
