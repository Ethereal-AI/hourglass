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
from dateutil import parser
from dateutil.relativedelta import relativedelta
import freezegun
from datetime import datetime
from typing import List, Dict, Union
from hourglass.utilities.detector import DateTimeEntityDetector

__author__ = "Ethereal AI"


class DateTimeTagger():
	def __init__(self, now: datetime = None):
		"""
		Builds the datetime tagger.

		Parameter
		---------
		now: datetime
			The datetime object to use as reference for the present.
		"""
		if now != None:
			use_freezegun = True
			dummy_present = now
		else:
			use_freezegun = False
			dummy_present = None
		self.use_freezegun = use_freezegun
		self.dummy_present = dummy_present

	def tag(self, texts: Union[List, str]) -> Union[Dict, List]:
		"""
		Tags the input text or texts via NER and regex rules.

		Parameter
		---------
		texts: Union[List, str]
			The input text or texts to be tagged.
		"""
		if isinstance(texts, str):
			detector = DateTimeEntityDetector()
			datetime_entities = detector.get_datetime_entities(texts)
		elif isinstance(texts, List):
			datetime_entities = list(map(lambda text: [self.tag(text)], texts))
		return datetime_entities
