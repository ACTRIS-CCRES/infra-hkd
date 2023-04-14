from enum import Enum
from typing import Dict, Any
import json
from grafanalib._gen import DashboardEncoder
class AcceptableCodes(Enum):
    OK = 200  # Ok
    POSTACCEPTED = 202
    EXISTS = 409  # Already created
    CREATED = 412  # Created by someone else

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

def get_encodable_dict(obj:Dict[Any,Any])->Dict[Any,Any]:
    """Get encodable dictionnary

    We need to dump it to ensure the DashboardEncoder execution that call 
    to_json_data on every child
    We need to reload it since the data or json does not work with `requests`.
    The behaviour is not really the same between `requests` and `json`
    Parameters
    ----------
    obj : Dict[Any,Any]
        Incoming dictionnary

    Returns
    -------
    Dict[Any,Any]
        the encodable dictionnary.
    """
    json_str = json.dumps(obj, sort_keys=True, indent=2, cls=DashboardEncoder)
    json_dict:Dict[Any,Any] = json.loads(json_str)

    return json_dict