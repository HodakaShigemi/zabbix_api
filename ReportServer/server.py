from wtforms.fields import SelectField, StringField, BooleanField, SubmitField
from bottle import route, run, template, request, static_file

class ItemHistoryForm(Form):
    item = SelectField(description='Item', coerce = str)
    time_from = StringField(description='Time from')
    time_till = StringField(description='Time till')
    submit = SubmitField('Download CSV')

class ReportForm(Form):
    screen = BooleanField(description='Screens', render_kw={'type':'checkbox'})
    submit = SubmitField('Download ZIP')


