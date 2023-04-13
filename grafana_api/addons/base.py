from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class GrafanaValidator:
    """This serializer is used to validate dataclass

    By subclassing this class, you can then use two methods :
    - validate_<attrs> to validate the data just after instantiating the dataclass for the <attrs>
    - validate : Validate method called after the validate_<attrs> methods
    """
    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            method = getattr(self, f"validate_{name}", None)
            if method:
                setattr(self, name, method(getattr(self, name), field=field))

        if hasattr(self, "validate"):
            self.validate()
