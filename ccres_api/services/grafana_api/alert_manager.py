from typing import Any, Dict, List, Optional, Union

import requests
from .base import AcceptableCodes, get_encodable_dict
from grafanalib.core import AlertGroup
from pprint import pprint as print


def _find_pos_of_alert_group(grafana_json_folder_copy: Dict[Any, Any], group) -> Optional[int]:
    """Find position of the alert group in the original grafana JSON"""
    for i, alert_group in enumerate(grafana_json_folder_copy):
        for value in alert_group.values():
            if group.get("name") == value:
                return i
    return None


def _find_pos_of_alert(alert_group_json: Dict[Any, Any], group) -> Optional[int]:
    """Find position of the alert in the alert group of the original grafana JSON"""
    for i, alert in enumerate(alert_group_json):
        if alert["grafana_alert"]["title"] == group["grafana_alert"]["title"]:
            return i
    return None


def _insert_into_existing_json(grafana_json_copy, folder, alert_group):
    """
    Insert json into the original grafana json and extract the sub folder JSON.
    """
    # TODO: Finish this :
    # Get this error
    # b'{"message":"failed to update rule group: failed to add rules: a conflicting alert rule is
    # found: rule title under the same organisation and folder should be unique","traceID":""}'
    alert_group_json = get_encodable_dict(alert_group)

    if folder not in grafana_json_copy:
        grafana_json_copy[folder] = alert_group_json
        return grafana_json_copy

    alert_group_position = _find_pos_of_alert_group(grafana_json_copy[folder], alert_group)
    if alert_group_position is None:
        grafana_json_copy[folder].append(alert_group_json)
        return grafana_json_copy

    for rule in alert_group["rules"]:
        alert_position = _find_pos_of_alert(
            grafana_json_copy[folder][alert_group_position]["rules"],
            rule,
        )
        if alert_position is None:
            grafana_json_copy[folder][alert_group_position]["rules"].append(rule)
            return grafana_json_copy

        grafana_json_copy[folder][alert_group_position]["rules"][alert_position] = rule

    return grafana_json_copy


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
        self._alerts: Dict[Any, Any] = {}

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

        if folder not in self._alerts:
            self._alerts[folder] = []

        self._alerts[folder].append(alert_dict)

    def _push_with_deleting(self) -> Dict[str, requests.Response]:
        """
        Pushes the alert data to Grafana, deleting any existing alerts in the same folder
        before creating new ones.

        Returns:
            requests.Response: Response object from the POST request.
        """
        responses = {}
        for folder, alert_groups in self._alerts.items():
            folder_removed = []
            if folder not in folder_removed:
                self.session.delete(f"{self.endpoint}/{folder}")
                folder_removed.append(folder)

            self.session.post(f"{self.endpoint_folders}", json={"title": folder})

            full_json_to_send = {}
            for alert_group in alert_groups:
                alert_group_json = get_encodable_dict(alert_group)
                if full_json_to_send == {}:
                    full_json_to_send = alert_group_json
                    continue

                for rule in alert_group_json.get("rules", []):
                    if any(
                        existing_rule["grafana_alert"]["title"] == rule["grafana_alert"]["title"]
                        for existing_rule in full_json_to_send.get("rules", [])
                    ):
                        continue

                    full_json_to_send["rules"].append(rule)

            res: requests.Response = self.session.post(
                f"{self.endpoint}/{folder}", json=full_json_to_send
            )
            responses[folder] = res
        return responses

    def _push_without_deleting(self) -> Dict[str, requests.Response]:
        """
        Pushes the alert data to Grafana without deleting any existing alerts.
        The new alerts will be added to the existing ones in the same folder.

        Returns:
            requests.Response: Response object from the POST request.
        """
        responses = {}
        for folder, alert_groups in self._alerts.items():
            self.session.post(f"{self.endpoint_folders}", json={"title": folder})

            full_json_to_send = self.fetched_json.copy()
            for alert_group in alert_groups:
                full_json_to_send = _insert_into_existing_json(
                    full_json_to_send, folder, alert_group
                )
            # Need to access the 0 element since grafana response is a list
            # containing  one element
            res: requests.Response = self.session.post(
                f"{self.endpoint}/{folder}", json=full_json_to_send[folder][0]
            )
            responses[folder] = res
        return responses

    def delete_folder(self, folder: str) -> requests.Response:
        response: requests.Response = self.session.delete(f"{self.endpoint}/{folder}")
        print(response.content)
        if response.status_code not in AcceptableCodes.list():
            msg = f"Error pushing the folder {folder} : "
            msg += f"[{response.status_code}] : {response.content}"
            raise requests.HTTPError(msg)
        return response

    def push(self, delete_existing: bool = False) -> requests.Response:
        """
        Pushes the alert data to Grafana based on the delete_existing flag.

        Args:
            delete_existing (bool): If True, delete any existing alerts before pushing new ones.
                                    If False, add new alerts to the existing ones.

        Returns:
            requests.Response: Response object from the POST request.

        Raises:
            requests.HTTPError: If the response status code is not in the acceptable list.
        """
        if delete_existing:
            responses = self._push_with_deleting()
        else:
            responses = self._push_without_deleting()

        for folder, response in responses.items():
            if response.status_code not in AcceptableCodes.list():
                msg = f"Error pushing the folder {folder} : "
                msg += f"[{response.status_code}] : {response.content}"
                raise requests.HTTPError(msg)
        return responses
