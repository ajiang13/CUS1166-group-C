from wtforms import Form, StringField, SelectField, SubmitField
from wtforms.widgets import html_params, HTMLString

class WelcomeForm(Form):
    search = SubmitField('Search for businesses')
    login = SubmitField('Login')

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

class ButtonWidget(object):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """
    input_type = 'submit'

    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=field.name, **kwargs),
            label=field.label.text)
        )


class ButtonField(StringField):
    widget = ButtonWidget()

class FilterForm(Form):
    choices = [('Name', 'Name'), ('City', 'City'), ('State', 'State'), ('Stars', 'Stars'), ('Reviews', 'Reviews')]
    button_ascending = ButtonField('Sort - Ascending')
    button_descending = ButtonField('Sort - Descending')
    select = SelectField('Sort by: ', choices = choices)
