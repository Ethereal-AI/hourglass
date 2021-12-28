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

__author__ = "Ethereal AI"


class DateTimeTagger():
	def __init__(self, now: datetime.datetime = None):
		"""
		Builds the datetime tagger.

		Parameter
		---------
		now: datetime.datetime
			The datetime object to use as
		"""
		if now not None:
			use_freezegun = True
			dummy_present = now
		else:
			use_freezegun = False
			dummy_present = None
		self.use_freezegun = use_freezegun
		self.dummy_present = dummy_present