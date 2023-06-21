from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union

@dataclass
class InfluxSource:
    url: str
    bucket: str
    tag: str


@dataclass
class Parameter:
    name: str
    influx_source: InfluxSource


class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class Alert:
    name: str
    summary: str
    description: str
    parameter: Parameter
    severity: Severity
