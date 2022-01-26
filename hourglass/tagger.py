# MIT License
# hourglass
# Copyright (c) 2022 Ethereal AI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""hourglass datetime tagger class"""
from datetime import datetime
from typing import List, Dict, Tuple, Union
from hourglass.utilities.detector import DateTimeEntityDetector
from hourglass.utilities.rule_parser import get_datetime_object, load_rules

__author__ = "Ethereal AI"


class DateTimeTagger:
    def __init__(self, now: datetime = None):
        """
        Builds the datetime tagger.

        Parameter
        ---------
        now: datetime
                The datetime object to use as reference for the present.
        """
        if now != None:
            dummy_present = now
        else:
            dummy_present = None
        self.dummy_present = dummy_present
        self.rules = load_rules()

    def fetch_with_dummy(self, datetime_entities, datetime_objects):
        if isinstance(datetime_entities, Tuple):
            datetime_objects = get_datetime_object(
                datetime_entities[0], self.dummy_present, self.rules
            )
        elif isinstance(datetime_entities, List):
            for substructure in datetime_entities:
                if isinstance(substructure, List):
                    datetime_objects.append(
                        self.fetch_all_datetime_objects(substructure)
                    )
                else:
                    datetime_objects.append(
                        get_datetime_object(
                            substructure[0], self.dummy_present, self.rules
                        )
                    )
        return datetime_objects

    def fetch_without_dummy(self, datetime_entities, datetime_objects):
        if isinstance(datetime_entities, Tuple):
            datetime_objects = get_datetime_object(
                datetime_entities[0], datetime.now(), self.rules
            )
        elif isinstance(datetime_entities, List):
            for substructure in datetime_entities:
                if isinstance(substructure, List):
                    datetime_objects.append(
                        self.fetch_all_datetime_objects(substructure)
                    )
                else:
                    datetime_objects.append(
                        get_datetime_object(substructure[0], datetime.now(), self.rules)
                    )
        return datetime_objects

    def fetch_all_datetime_objects(
        self, datetime_entities: Union[Tuple, List]
    ) -> Union[List, datetime]:
        datetime_objects = list()
        if self.dummy_present != None:
            datetime_objects = self.fetch_with_dummy(
                datetime_entities, datetime_objects
            )
        else:
            datetime_objects = self.fetch_without_dummy(
                datetime_entities, datetime_objects
            )
        return datetime_objects

    def tag(self, texts: Union[List, str]) -> Union[List, datetime]:
        """
        Tags the input text or texts via NER and rule rules.

        Parameter
        ---------
        texts: Union[List, str]
                The input text or texts to be tagged.
        """
        detector = DateTimeEntityDetector()
        if isinstance(texts, str):
            datetime_entities = detector.get_datetime_entities(texts)
            datetime_objects = self.fetch_all_datetime_objects(datetime_entities)
            return datetime_objects
        elif isinstance(texts, List) and len(texts) == 1:
            datetime_entities = detector.get_datetime_entities(texts[0])
            datetime_objects = self.fetch_all_datetime_objects(datetime_entities)
            return datetime_objects
        elif isinstance(texts, List) and len(texts) > 1:
            datetime_objects = list(map(lambda text: [self.tag(text)], texts))
            datetime_objects = [
                datetime_object[0]
                if isinstance(datetime_object[0], List)
                else datetime_object
                for datetime_object in datetime_objects
            ]
            return datetime_objects
