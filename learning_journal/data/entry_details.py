"""List of all learing journal entries."""


from datetime import datetime

FMT = "%m/%d/%Y %I:%M %p"
ENTRIES = [
    {
        'id': 1,
        'title': "Day One",
        'creation_date': datetime.strptime('10/16/2017 4:18 PM', FMT),
        'body': """<p>