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
"""hourglass regex parser functions"""
import json
from hourglass.utilities.paths import RULES_PATH
from dateutil.relativedelta import relativedelta

def get_relativedelta_function(unit: str, value: int) -> relativedelta:
	if unit == "microseconds":
		return relativedelta(microseconds=value)
	elif unit == "seconds":
		return relativedelta(seconds=value)
	elif unit == "minutes":
		return relativedelta(minutes=value)
	elif unit == "hours":
		return relativedelta(hours=value)
	elif unit == "days":
		return relativedelta(days=value)
	elif unit == "weeks":
		return relativedelta(weeks=value)
	elif unit == "months":
		return relativedelta(months=value)
	elif unit == "years":
		return relativedelta(years=value)
	elif unit == "decades":
		return relativedelta(years=value*10)
	elif unit == "centuries":
		return relativedelta(years=value*100)
	else:
		return None

def load_rules():
	rules = dict()
	with open(RULES_PATH) as f:
		for line in f:
			rule = json.loads(line)
			properties = {"operation": rule.get("operation"), "relativedelta_function": get_relativedelta_function(rule.get("relativedelta"), rule.get("value"))}
			rules[rule.get("pattern")] = properties
	return rules