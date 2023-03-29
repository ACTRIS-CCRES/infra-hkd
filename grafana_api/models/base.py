from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class GrafanaSerializer:
    """This serializer is used to convert dataclass to JSON

    By subclassing this class, you can then use two methods :
    validate_<attrs> to validate the data just after instantiating the dataclass
    convert_<attrs> to convert the data when convert to json with get_camel_case_json
    """

    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        if hasattr(self, "validate"):
            self.validate()

        for name, field in self.__dataclass_fields__.items():
            method = getattr(self, f"validate_{name}", None)
            if method:
                setattr(self, name, method(getattr(self, name), field=field))

    def get_cleaned_key(self, key: str) -> Optional[str]:
        if key in ["remove_first_underscore"]:
            return None

        to_clean = hasattr(self, "remove_first_underscore") and key in getattr(
            self, "remove_first_underscore"
        )
        if to_clean and key.startswith("_"):
            key = key[1:]
        return key

    def _serialize(self, key: str) -> Any:
        value = getattr(self, key)
        converted_value: Any = value

        if hasattr(self, f"convert_{key}"):
            method = getattr(self, f"convert_{key}")
            converted_value = method()

        if hasattr(value, "serialize"):
            converted_value = converted_value.serialize()

        if isinstance(converted_value, list):
            for i, el in enumerate(value):
                if isinstance(el, GrafanaSerializer):
                    converted_value[i] = el.serialize()

        if isinstance(converted_value, dict):
            for key, _value in converted_value.items():
                if isinstance(_value, GrafanaSerializer):
                    converted_value[key] = _value.serialize()

        return converted_value

    def serialize(self) -> Any:
        """Convert the dataclass the a CamelCase JSON

        Convert to :
        {CamelCaseAttribute: value}

        It try to execute the convert_<attr> method on the value if present.
        """
        _json = {}
        for key, _ in self.__annotations__.items():

            json_value = self._serialize(key)
            if json_value is None:
                continue

            cleaned_key = self.get_cleaned_key(key)
            if cleaned_key is None:
                continue

            _json[cleaned_key] = json_value

        return _json
