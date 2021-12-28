# hourglass

Detect and parse date-time entities in text.

### Installing the package

Option 1:<br>
1. Clone the repository and run `python setup.py build` and then `python setup.py install`.<br>
2. Run `python -m spacy download en_core_web_sm`.<br><br>
Option 2:<br>
1. Run pip install git+ssh://git@github.com:Ethereal-AI/hourglass.git<br>
2. Run `python -m spacy download en_core_web_sm`.<br><br>

### Usage

To use the main tagging function run the following code:
```python
from hourglass.tagger import DateTimeTagger

dtt = DateTimeTagger()
print(dtt.tag("I had an appointment 2 days ago. My next one is tomorrow. 10 days from now, I would be fully vaccinated."))

>>> [{'entity': 'an appointment 2 days ago', 'parsed_value': datetime.datetime(2021, 12, 26, 22, 28, 20, 951975)}, {'entity': 'tomorrow', 'parsed_value': datetime.datetime(2021, 12, 29, 22, 28, 20, 951975)}, {'entity': '10 days', 'parsed_value': datetime.datetime(2022, 1, 7, 22, 28, 20, 951975)}]
```