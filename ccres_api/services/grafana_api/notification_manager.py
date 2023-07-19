from typing import Any, Dict, Union

import requests
from .addons.contact import ContactPoint
from .addons.notification_policies import Notification
from .base import AcceptableCodes, get_encodable_dict


class NotificationManager:
    """Class that handle the creation of contact point and notification policy

    We can add multiple contact points or notification policies and then we push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/alertmanager/grafana/config/api/v1/alerts"
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

    def add_contact_point(
        self, contact_point: Union[ContactPoint, Dict[Any, Any]]
    ) -> "NotificationManager":
        if isinstance(contact_point, ContactPoint):
            name = contact_point.name
            contact_dict = contact_point.to_json_data()
        else:
            name = contact_point["name"]
            contact_dict = contact_point

        _contact_exists = False
        _contact_idx = 0
        for idx, contact in enumerate(self.to_push_json["alertmanager_config"]["receivers"]):
            if "name" not in contact:
                continue
            if contact["name"] == name:
                _contact_exists = True
                _contact_idx = idx

        if not _contact_exists:
            self.to_push_json["alertmanager_config"]["receivers"].append(
                {
                    "grafana_managed_receiver_configs": [contact_dict],
                    "name": name,
                },
            )
        else:
            self.to_push_json["alertmanager_config"]["receivers"][_contact_idx][
                "grafana_managed_receiver_configs"
            ] = [contact_dict]

        return self

    def add_notification_policy(
        self, notification_policy: Union[Notification, Dict[Any, Any]]
    ) -> "NotificationManager":
        if isinstance(notification_policy, Notification):
            notification_dict = notification_policy.to_json_data()
        else:
            notification_dict = notification_policy
        self.to_push_json["alertmanager_config"]["route"]["routes"].append(notification_dict)
        return self

    def push(self) -> requests.Response:
        json_d = get_encodable_dict(self.to_push_json)
        res: requests.Response = self.session.post(self.endpoint, json=json_d)
        if res.status_code not in AcceptableCodes.list():
            msg = f"[{res.status_code}] : {res.content}"
            if res.status_code == 400:
                msg += "\nMaybe the contact point does not exist ?"
            raise requests.HTTPError(msg)
        return res
