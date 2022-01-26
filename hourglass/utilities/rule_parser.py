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
from word2number import w2n


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
    if len(tag_tail) != 0:
        tag_tail_string = " " + " ".join(tag_tail)
    else:
        tag_tail_string = ""
    if plurality == "singular":
        rule_query = (
            f"{tag_head_string}<int> {token}({UNITS_PLURAL[index]}){tag_tail_string}"
        )
    elif plurality == "plural":
        rule_query = (
            f"{tag_head_string}<int> {UNITS_SINGULAR[index]}({token}){tag_tail_string}"
        )
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


def get_dt_singular(token, tokens, rules, present):
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
    return datetime_object


def get_datetime_object(tag: str, present: datetime, rules: Dict) -> List:
    try:
        rule = rules.get(tag)
        datetime_object = compute_datetime(rule, present)
        return {"entity": tag, "parsed_value": datetime_object}
    except:
        tokens = tokenize(tag)
        for idx, token in enumerate(tokens):
            if token in UNITS_SINGULAR:
                datetime_object = get_dt_singular(token, tokens, rules, present)
                return {"entity": tag, "parsed_value": datetime_object}
            elif token in UNITS_PLURAL:
                value = tokens[idx - 1]
                try:
                    tag_head = tokens[: idx - 1]
                except:
                    tag_head = []
                rule = get_custom_rule(
                    rules,
                    token,
                    UNITS_PLURAL.index(token),
                    tag_head,
                    tokens[idx + 1 :],
                    "plural",
                )
                datetime_object = compute_datetime(
                    rule,
                    present,
                    UNITS_PLURAL[UNITS_PLURAL.index(token)],
                    special_value=value,
                )
                return {"entity": tag, "parsed_value": datetime_object}
