from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union
from .base import GrafanaValidator
from .utils import clean_none

class GrafanaMatchType(str, Enum):
    EQUAL = "="
    NOT_EQUAL = "="
    MATCH_REGEX = "=~"
    DOESNT_MATCH_REGEX = "!~"


@dataclass
class RegexMatcher(GrafanaValidator):
    """Model to match the labels and raise alert

    Parameters
    ----------
    name: str
        Name of the label
    type: GrafanaMatchType
        How to compare label with the value
    value: str
        Value of the label

    """
    name: str
    type: Union[str,GrafanaMatchType]
    value: str

    def to_json_data(self):
        _type = self.type
        if isinstance(self.type, Enum):
            _type = _type.value
        return [self.name, _type, self.value]


@dataclass
class Notification(GrafanaValidator):
    """Notification policies model


    Parameters
    ----------
    receiver: Optional[str]
        Name of the notification, by default None
    object_matchers: Optional[List[RegexMatcher]]
        Labels to match the policy to. Label Operator Value, by default None
    do_continue: Optional[str]
        by default None
    group_by: Optional[List[str]]
        by default None
    group_interval: Optional[str]
        by default None
    group_wait: Optional[str]
        by default None
    match_re: Optional[str]
        by default None
    matchers: Optional[str]
        by default None
    mute_time_intervals: Optional[str]
        by default None
    provenance: Optional[str]
        by default None
    repeat_interval: Optional[str]
        by default None
    routes: Optional[str]
        by default None
    """
    receiver: Optional[str] = None
    object_matchers: Optional[List[RegexMatcher]] = None
    do_continue: Optional[str] = None
    group_by: Optional[List[str]] = None
    group_interval: Optional[str] = None
    group_wait: Optional[str] = None
    match_re: Optional[str] = None
    matchers: Optional[str] = None
    mute_time_intervals: Optional[str] = None
    provenance: Optional[str] = None
    repeat_interval: Optional[str] = None
    routes: Optional[str] = None

    def to_json_data(self):
        json_data = {
            "receiver": self.receiver,
            "object_matchers": [obj.to_json_data() for obj in self.object_matchers],
            "_continue": self.do_continue,
            "groupBy": self.group_by,
            "groupInterval": self.group_interval,
            "groupWait": self.group_wait,
            "matchRe": self.match_re,
            "matchers": self.matchers,
            "muteTimeIntervals": self.mute_time_intervals,
            "provenance": self.provenance,
            "repeatInterval": self.repeat_interval,
            "routes": self.routes,
        }
        return clean_none(json_data)
