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
"""hourglass detection functions"""
from typing import Dict

import spacy

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
