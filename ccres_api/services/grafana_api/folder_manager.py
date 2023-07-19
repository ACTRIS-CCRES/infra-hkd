from typing import Any, Dict, Union, List

import requests
from .addons.folder import Folder
from .addons.notification_policies import Notification
from .base import AcceptableCodes, get_encodable_dict


class FolderManager:
    """Class that handle the creation of folder

    We can add multiple folders and then push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/folders/"
        self.fetched_json: Dict[Any, Any] = self.fetch()
        self._folders = []

    def get_fetched_json(self) -> Any:
        return self.fetched_json

    def fetch(self) -> Dict[Any, Any]:
        res = self.session.get(self.endpoint)
        if res.status_code not in AcceptableCodes.list():
            msg = "Unable to get the current configuration\n"
            msg += f"[{res.status_code}] : {res.content}"
            raise requests.HTTPError(msg)
        self.fetched_json = res.json()
        return self.fetched_json

    def add_folder(self, folder: Union[Folder, Dict[Any, Any]]) -> "FolderManager":
        if isinstance(folder, Folder):
            folder_dict = folder.to_json_data()
        else:
            folder_dict = folder

        self._folders.append(folder_dict)

        return self

    def push(self) -> List[requests.Response]:
        responses = []
        for folder in self._folders:
            json_d = get_encodable_dict(folder)

            res: requests.Response = self.session.post(self.endpoint, json=json_d)
            if res.status_code not in AcceptableCodes.list():
                msg = f"[{res.status_code}] : {res.content}"
                raise requests.HTTPError(msg)
            responses.append(res)
        return responses
