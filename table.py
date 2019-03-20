from flask_table import Table, Col

class Restaurant Info(Table):
    id = Col('Id', show=False)
    Name = Col('Name')
    City = Col('City')
    State = Col('State')
    Stars = Col('Stars')
    Postal_Code = Col('Postal_Code')
