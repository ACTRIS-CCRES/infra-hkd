from typing import Any, Dict, List, Optional, Union

import requests
from .base import AcceptableCodes, get_encodable_dict
from grafanalib.core import AlertGroup


def _find_pos_of_alert_group(grafana_json_copy: Dict[Any, Any], group) -> Optional[int]:
    """Find position of the alert group in the original grafana JSON"""
    for alert_group in grafana_json_copy:
        for i, value in enumerate(alert_group.values()):
            print(value)
            if group.get("name") == value:
                return i
    return None


def _find_pos_of_alert(alert_group_json: Dict[Any, Any], group) -> Optional[int]:
    """Find position of the alert in the alert group of the original grafana JSON"""
    for i, alert in enumerate(alert_group_json):
        print(alert)
        print(group)
        if alert["grafana_alert"]["title"] == group["grafana_alert"]["title"]:
            return i
    return None


def _insert_into_existing_json(grafana_json_copy, folder, alert_group, json_d):
    """Insert json into the original grafana json and extract the sub folder JSON"""
    if folder in grafana_json_copy:
        alert_group_position = _find_pos_of_alert_group(grafana_json_copy[folder], alert_group)
        if alert_group_position is not None:
            alert_position = _find_pos_of_alert(
                grafana_json_copy[folder][alert_group_position]["rules"],
                alert_group["rules"][0],
            )
            if alert_position is not None:
                grafana_json_copy[folder][alert_group_position]["rules"][alert_position] = json_d[
                    "rules"
                ][0]
            else:
                grafana_json_copy[folder][alert_group_position]["rules"].append(json_d["rules"][0])
        else:
            grafana_json_copy[folder].append(json_d)
    else:
        grafana_json_copy[folder] = [json_d]
    return grafana_json_copy[folder][0]


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
        grafana_json_copy = self.fetched_json.copy()

        for alert in self._alerts:
            for folder in alert:
                self.session.post(f"{self.endpoint_folders}", json={"title": folder})
                for alert_group in alert[folder]:
                    json_d = get_encodable_dict(alert_group)
                    json_d = _insert_into_existing_json(
                        grafana_json_copy, folder, alert_group, json_d
                    )

                    res: requests.Response = self.session.post(
                        f"{self.endpoint}/{folder}", json=json_d
                    )
                    if res.status_code not in AcceptableCodes.list():
                        raise requests.HTTPError(f"[{res.status_code}] : {res.content}")
                responses.append(res)
        return responses
