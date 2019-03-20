from wtforms import Form, StringField, SelectField

class SearchForm(Form):
    choices = [('Name', 'Name'), ('ID', 'ID'), ('City', 'City'), ('Stars', 'Stars'), ('Categories', 'Categories')]
    select = SelectField('Search for restaurants:', choices=choices)
    search = StringField('')
