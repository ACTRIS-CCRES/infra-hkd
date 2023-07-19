from dataclasses import dataclass
from typing import Optional
from .base import GrafanaValidator
from .utils import clean_none


@dataclass
class Folder(GrafanaValidator):
    """Contact point setting for Email

    Parameters
    ----------

    name: str
        Name of the folder
    uid: Optional[str], by default None
        Force the UID
    """

    name: str
    uid: Optional[str] = None

    def to_json_data(self):
        json_data = {
            "title": self.name,
            "uid": self.uid,
        }
        return clean_none(json_data)
