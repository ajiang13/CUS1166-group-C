from flask_table import Table, Col, LinkCol

class Results(Table):
    business_id = Col('Id', show=False)
    name = Col('Name')
    address = Col('Address')
    city = Col('City')
    state = Col('State')
    postal_code = Col('Zip Code')
    latitude = Col('Latitude')
    longitude = Col('Longitude')
    stars = Col('Stars')
    review_count = Col('Reviews')
    is_open = Col('Open')
    attributes = Col('Attributes')
    categories = Col('Categories')
    hours = Col('Hours')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
