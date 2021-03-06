from wtforms import StringField, SelectField, TextField, FloatField, \
    PasswordField, validators
from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    choices = [('Name', 'Name'),
               ('City', 'City'),
               ('State', 'State Code'),
               ('Categories', 'Categories')]
    select = SelectField('Search for restaurants:', choices=choices)
    search = StringField('')
    stars = FloatField('Search by rating e.g. 4.5 (and above):')


class AdvancedSearchForm(FlaskForm):
    name = StringField('Name')
    city = StringField('City')
    state = StringField('State Code')
    categories = StringField('Categories')
    stars = FloatField('Rating')


class RegistrationForm(FlaskForm):
    name = [StringField('Name', [validators.Length(min=1, max=100)])]
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField(
              'New Password',
              [validators.DataRequired(),
               validators.EqualTo(
               'confirm',
               message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


class LoginForm(FlaskForm):
    username = StringField(
              'username',
              [validators.DataRequired(),
               validators.Length(min=1, max=100)])
    password = PasswordField(
              'password',
              [validators.DataRequired(),
               validators.Length(min=1, max=100)])


class FilterForm(FlaskForm):
    choices = [('Name', 'Name'),
               ('City', 'City'),
               ('State', 'State'),
               ('Stars', 'Stars'),
               ('Reviews', 'Reviews')]
    select = SelectField('Sort by: ', choices=choices)


class DisplayForm(FlaskForm):
    hours = StringField('Hours')
    latitude = StringField('Latitude')
    longitude = StringField('Longitude')


class RestaurantForm(FlaskForm):
    name = StringField('Name')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('Zip Code')
    categories = StringField('Categories')


class MailForm(FlaskForm):
    recipients = StringField(
                'Recipient(s)',
                [validators.InputRequired()])
    body = StringField('Body')


class RandomForm(FlaskForm):
    random = "Can't decide? Generate a random restaurant!"
