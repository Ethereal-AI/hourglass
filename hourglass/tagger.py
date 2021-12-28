# hourglass
# Copyright (C) 2021 Ethereal AI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
