from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from base import GrafanaSerializer, AcceptableCodes


class GrafanaMatchType(str, Enum):
    EQUAL = "="
    NOT_EQUAL = "="
    MATCH_REGEX = "=~"
    DOESNT_MATCH_REGEX = "!~"


@dataclass
class GrafanaRegexpsMatcherModel(GrafanaSerializer):
    name: str
    type: GrafanaMatchType
    value: str

    def serialize(self) -> Any:
        _type = self.type
        if isinstance(self.type, Enum):
            _type = _type.value
        return [self.name, _type, self.value]


@dataclass
class GrafanaRouteModel(GrafanaSerializer):
    # Name of the contact point
    receiver: Optional[str] = None
    # Tags to be used
    object_matchers: Optional[List[GrafanaRegexpsMatcherModel]] = None
    _continue: Optional[str] = None
    groupBy: Optional[List[str]] = None
    groupInterval: Optional[str] = None
    groupWait: Optional[str] = None
    matchRe: Optional[str] = None
    matchers: Optional[str] = None
    muteTimeIntervals: Optional[str] = None
    provenance: Optional[str] = None
    repeatInterval: Optional[str] = None
    routes: Optional[str] = None
    remove_first_underscore: List[str] = field(default_factory=lambda: ["_continue"])
