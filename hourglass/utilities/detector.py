# hourglass
# Copyright (C) 2021-2022 Ethereal AI
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
"""hourglass detection functions"""
import spacy
from typing import Dict

__author__ = "Ethereal AI"


class DateTimeEntityDetector:
    def __init__(self):
        self.model = spacy.load(
            "en_core_web_sm",
            disable=["attribute_ruler", "lemmatizer", "parser", "tagger"],
        )

    def get_datetime_entities(self, text) -> Dict:
        entity_labels = ("DATE", "TIME")
        tagged_entities = self.model(text)
        datetime_entities = [
            (ent.text, ent.start_char, ent.end_char, ent.label_)
            for ent in tagged_entities.ents
            if (ent.label_ in entity_labels)
        ]
        if len(datetime_entities) != 1:
            return datetime_entities
        else:
            return datetime_entities[0]
