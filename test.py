from hourglass.tagger import DateTimeTagger

# from hourglass.utilities.regex_parser import get_datetime_object, load_rules
from datetime import datetime

dtt = DateTimeTagger()
print(dtt.tag("I had an appointment 2 days ago and another one a day ago. My next one is tomorrow."))

# rules = load_rules()
# print(get_datetime_object("yesterday", datetime.now(), rules))
