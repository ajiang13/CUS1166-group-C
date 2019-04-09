from wtforms import StringField, SelectField, TextField, FloatField, PasswordField, validators
from flask_wtf import Form

class SearchForm(Form):
    choices = [('Name', 'Name'), ('City', 'City'), ('State', 'State Code'), ('Categories', 'Categories')]
    select = SelectField('Search for restaurants:', choices=choices)
    search = StringField('')
    stars = FloatField('Search by rating e.g. 4.5 (and above):')

class AdvancedSearchForm(Form):
    name = StringField('Name')
    city = StringField('City')
    state = StringField('State Code')
    categories = StringField('Categories')
    stars = FloatField('Rating')

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class DisplayForm(Form):
    hours = StringField('Hours')
    latitude = StringField('Latitude')
    longitude = StringField('Longitude')

class FilterForm(Form):
    choices = [('Name', 'Name'), ('City', 'City'), ('State', 'State'), ('Stars', 'Stars'), ('Reviews', 'Reviews')]
    select = SelectField('Sort by: ', choices = choices)

class RestaurantForm(Form):
    is_open = [('Open', 'Open'), ('Closed','Closed')]
    name = StringField('Name')
    city = StringField('City')
    state = StringField('State')
    categories = StringField('Categories')
    latitude = StringField('latitude')
    longitude = StringField('longitude')
    hours = StringField('hours')
    categories = StringField('categories')
    is_open = SelectField('Availability', choices=is_open)
