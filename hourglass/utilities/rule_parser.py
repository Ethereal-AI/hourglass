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
"""hourglass rule parser functions"""
import json
from hourglass.utilities.paths import RULES_PATH
from hourglass.utilities.rule_helper_functions import (
    UNITS_PLURAL,
    UNITS_SINGULAR,
    tokenize,
)
from dateutil.relativedelta import relativedelta
from datetime import datetime
from typing import List, Dict


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
        return relativedelta(years=value * 10)
    elif unit == "centuries":
        return relativedelta(years=value * 100)
    else:
        return None


def load_rules():
    rules = dict()
    with open(RULES_PATH) as f:
        for line in f:
            rule = json.loads(line)
            if isinstance(rule.get("value"), str):
                value = 0
            else:
                value = rule.get("value")
            properties = {
                "operation": rule.get("operation"),
                "relativedelta_function": get_relativedelta_function(
                    rule.get("relativedelta"), value
                ),
            }
            rules[rule.get("pattern")] = properties
    return rules


def get_custom_rule(rules, token, index, tag_head, tag_tail, plurality="singular"):
    if len(tag_head) != 0:
        tag_head_string = " ".join(tag_head) + " "
    else:
        tag_head_string = ""
    print(tag_head_string)
    if len(tag_tail) != 0:
        tag_tail_string = " " + " ".join(tag_tail)
    else:
        tag_tail_string = ""
    if plurality == "singular":
        rule_query = f"{tag_head_string}<int> {token}({UNITS_PLURAL[index]}){tag_tail_string}"
    elif plurality == "plural":
        rule_query = f"{tag_head_string}<int> {UNITS_SINGULAR[index]}({token}){tag_tail_string}"
    if rule_query in rules:
        rule = rules.get(rule_query)
    else:
        if plurality == "singular":
            rule_query = f"<int> {token}({UNITS_PLURAL[index]}){tag_tail_string}"
        elif plurality == "plural":
            rule_query = f"<int> {UNITS_SINGULAR[index]}({token}){tag_tail_string}"
        if rule_query in rules:
            rule = rules.get(rule_query)
        else:
            rule = None
    return rule


def compute_datetime(rule, present: datetime, unit=None, special_value=None):
    if special_value == None:
        if rule.get("operation") == "-":
            return present - rule.get("relativedelta_function")
        elif rule.get("operation") == "+":
            return present + rule.get("relativedelta_function")
        else:
            return present
    else:
        if special_value == "a":
            special_value = 1
        if rule.get("operation") == "-":
            return present - get_relativedelta_function(unit, int(special_value))
        elif rule.get("operation") == "+":
            return present + get_relativedelta_function(unit, int(special_value))
        else:
            return present


def get_datetime_object(tag: str, present: datetime, rules: Dict) -> List:
    try:
        rule = rules.get(tag)
        datetime_object = compute_datetime(rule, present)
        return {"entity": tag, "parsed_value": datetime_object}
    except:
        tokens = tokenize(tag)
        for idx, token in enumerate(tokens):
            if token in UNITS_SINGULAR:
                value = tokens[idx - 1]
                try:
                    tag_head = tokens[: idx - 1]
                except:
                    tag_head = []
                rule = get_custom_rule(
                    rules,
                    token,
                    UNITS_SINGULAR.index(token),
                    tag_head,
                    tokens[idx + 1 :],
                    "singular",
                )
                datetime_object = compute_datetime(
                    rule,
                    present,
                    UNITS_PLURAL[UNITS_SINGULAR.index(token)],
                    special_value=value,
                )
                return {"entity": tag, "parsed_value": datetime_object}
            elif token in UNITS_PLURAL:
                value = tokens[idx - 1]
                try:
                    tag_head = tokens[: idx - 1]
                except:
                    tag_head = []
                rule = get_custom_rule(
                    rules, token, UNITS_PLURAL.index(token), tag_head, tokens[idx + 1 :], "plural"
                )
                datetime_object = compute_datetime(
                    rule,
                    present,
                    UNITS_PLURAL[UNITS_PLURAL.index(token)],
                    special_value=value,
                )
                return {"entity": tag, "parsed_value": datetime_object}
