from wtforms import Form, StringField, SelectField

class SearchForm(Form):
    choices = [('Name', 'Name'), ('ID', 'ID'), ('City', 'City'), ('Stars', 'Stars'), ('Categories', 'Categories')]
    select = SelectField('Search for restaurants:', choices=choices)
    search = StringField('')

#class RegistrationForm(Form):
    #username = TextField('Username', [validators.Length(min=4, max=20)])
    #email = TextField('Email Address', [validators.Length(min=6, max=50)])
    #password = PasswordField('New Password', [validators.Required(),
    #    validators.EqualTo('confirm', message='Passwords must match')
    #])
    #confirm = PasswordField('Repeat Password')

class FilterForm(Form):
    choices = [('Name', 'Name'), ('ID', 'ID'), ('City', 'City'), ('Stars', 'Stars'), ('Categories', 'Categories')]
    select = SelectField('Filter by: ', choices = choices)
