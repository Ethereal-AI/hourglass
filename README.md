# hourglass

Detect and parse date-time entities in text.

### Installing the package
1. Clone the repository.<br>
2. Run `pip install -e .` inside the local repository.<br>
3. Run `python -m spacy download en_core_web_sm`.<br><br>

### Usage

To use the main tagging function run the following code:
```python
from hourglass.tagger import DateTimeTagger

dtt = DateTimeTagger()
print(dtt.tag("I had an appointment 2 days ago. My next one is tomorrow. 10 days from now, I would be fully vaccinated."))

>>> [{'entity': 'an appointment 2 days ago', 'parsed_value': datetime.datetime(2021, 12, 27, 3, 16, 8, 220097)}, {'entity': 'tomorrow', 'parsed_value': datetime.datetime(2021, 12, 30, 3, 16, 8, 220097)}, {'entity': '10 days from now', 'parsed_value': datetime.datetime(2022, 1, 8, 3, 16, 8, 220097)}]
```

By instantiating `DateTimeTagger()` without specifying a `now` parameter, you provide the current system date and time as its default value. To set a dummy date-time object as the reference for `now`:

```python
from hourglass.tagger import DateTimeTagger
from datetime import datetime

dtt = DateTimeTagger(now=datetime(1998, 7, 17, 0, 0, 0, 0))
print(dtt.tag("I had an appointment 2 days ago. My next one is tomorrow. 10 days from now, I would be fully vaccinated."))

>>> [{'entity': 'an appointment 2 days ago', 'parsed_value': datetime.datetime(1998, 7, 15, 0, 0)}, {'entity': 'tomorrow', 'parsed_value': datetime.datetime(1998, 7, 18, 0, 0)}, {'entity': '10 days from now', 'parsed_value': datetime.datetime(1998, 7, 27, 0, 0)}]
``` 