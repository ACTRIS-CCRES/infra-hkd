from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class AcceptableCodes(Enum):
    OK = 200  # Ok
    POSTACCEPTED = 202
    EXISTS = 409  # Already created
    CREATED = 412  # Created by someone else

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))