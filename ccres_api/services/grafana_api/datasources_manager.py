from typing import Any, Dict

import requests
from .base import AcceptableCodes


class DatasourceManager:
    """Class that handle the creation of contact point and notification policy

    We can add multiple contact points or notification policies and then we push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/datasources/"
        self.fetched_json: Dict[Any, Any] = self.fetch()
        self.to_push_json = self.fetched_json.copy()

    def get_fetched_json(self) -> Dict[Any, Any]:
        return self.fetched_json

    def fetch(self) -> Dict[Any, Any]:
        res = self.session.get(self.endpoint)
        if res.status_code not in AcceptableCodes.list():
            msg = "Unable to get the current configuration\n"
            msg += f"[{res.status_code}] : {res.content}"
            raise requests.HTTPError(msg)
        self.fetched_json = res.json()
        return self.fetched_json
