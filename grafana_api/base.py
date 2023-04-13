from enum import Enum

class AcceptableCodes(Enum):
    OK = 200  # Ok
    POSTACCEPTED = 202
    EXISTS = 409  # Already created
    CREATED = 412  # Created by someone else

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))