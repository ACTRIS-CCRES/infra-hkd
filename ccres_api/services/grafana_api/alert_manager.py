from typing import Any, Dict, List, Optional, Union

import requests
from .base import AcceptableCodes, get_encodable_dict
from grafanalib.core import AlertGroup


class AlertManager:
    """Class that handle the creation of alert rules

    We can add multiple contact points or notification policies and then we push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/ruler/grafana/api/v1/rules"
        self.endpoint_folders = f"{self.url}/folders"
        self.fetched_json: Dict[Any, Any] = self.fetch()
        self._alerts = []

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

    def add_alert(
        self, alertgroup: Union[AlertGroup, Dict[Any, Any]], folder: Optional[str] = None
    ):
        if isinstance(alertgroup, AlertGroup):
            alert_dict = alertgroup.to_json_data()
        else:
            alert_dict = alertgroup

        if folder is None:
            folder = "Alerts"

        self._alerts.append({folder: [alert_dict]})

    def push(self) -> List[requests.Response]:
        responses = []
        for alert in self._alerts:
            for folder in alert:
                for group in alert[folder]:
                    json_d = get_encodable_dict(group)
                    self.session.post(f"{self.endpoint_folders}", json={"title": folder})
                    res: requests.Response = self.session.post(f"{self.endpoint}/{folder}", json=json_d)
                    if res.status_code not in AcceptableCodes.list():
                        raise requests.HTTPError(f"[{res.status_code}] : {res.content}")
                responses.append(res)
        return responses
