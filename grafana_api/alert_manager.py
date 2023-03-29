from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from base import GrafanaSerializer, AcceptableCodes
from grafana_api.models.contact import (
    GrafanaContactPointModelEmail,
    GrafanaContactPointModelEmailSettings,
)
from grafana_api.models.notification_policies import GrafanaRouteModel
from pprint import pprint as print
from grafana_api.models.alert import (
    ModelAlert,
    ModelAlertRule,
    ModelAlertRuleGrafanaAlertDataModel,
    ModelAlertRuleGrafanaAlert,
    ModelAlertRuleGrafanaAlertData,
    ModelAlertRuleGrafanaAlertDataModelCondition,
    ModelEvaluator,
    ModelOperator,
    ModelQuery,
    ModelReducer,
    GrafanaDatasource,
    GrafanaRelativeTimeRange,
    GrafanaDuration,
)


class GrafanaAlertManager:
    """Class that handle the creation of contact point and notification policy

    We can add multiple contact points or notification policies and then we push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/alertmanager/grafana/config/api/v1/alerts"

        res = self.session.get(self.endpoint)
        if res.status_code not in AcceptableCodes.list():
            msg = "Unable to get the current configuration\n"
            msg += f"[{res.status_code}] : {res.content}"
            raise requests.HTTPError(msg)
        self.config = res.json()

    def get(self) -> Any:
        return self.config

    def add_contact_point(
        self, contact_point: GrafanaContactPointModelEmail
    ) -> "GrafanaAlertManager":
        if isinstance(contact_point, GrafanaContactPointModelEmail):
            name = contact_point.name
            contact_dict = contact_point.serialize()
        else:
            name = contact_point["name"]
            contact_dict = contact_point

        self.config["alertmanager_config"]["receivers"].append(
            {
                "grafana_managed_receiver_configs": [contact_dict],
                "name": name,
            },
        )
        return self

    def add_notification_policy(
        self, notification_policy: GrafanaRouteModel
    ) -> "GrafanaAlertManager":
        if isinstance(notification_policy, GrafanaRouteModel):
            notification_dict = notification_policy.serialize()
        else:
            notification_dict = notification_policy

        self.config["alertmanager_config"]["route"]["routes"].append(notification_dict)
        return self

    def push(self) -> requests.Response:
        res: requests.Response = self.session.post(self.endpoint, json=self.config)
        if res.status_code not in AcceptableCodes.list():
            raise requests.HTTPError(f"[{res.status_code}] : {res.content}")
        return res


class GrafanaAlertRuleManager:
    """Class that handle the creation of alert rules

    We can add multiple contact points or notification policies and then we push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/ruler/grafana/api/v1/rules"
        self.config = self.session.get(f"{self.endpoint}").json()

    def add_alert(self, alert: ModelAlert):
        if isinstance(alert, ModelAlert):
            alert_dict = alert.serialize()
        else:
            alert_dict = alert

        if self.config == {}:
            self.config["Alerts"] = []
        for folder in self.config:
            existing_group = None
            for pos, _alert in enumerate(self.config[folder]):
                if _alert["name"] == alert_dict["name"]:
                    existing_group = (pos, _alert["name"])
                    break
            # Add group to config
            if existing_group is None:
                self.config[folder].append(alert_dict)
            # Add rules to group
            else:
                self.config[folder][existing_group[0]]["rules"].extend(alert_dict["rules"])

    def push(self) -> List[requests.Response]:
        responses = []
        for folder in self.config:
            for group in self.config[folder]:
                res: requests.Response = self.session.post(f"{self.endpoint}/{folder}", json=group)
                if res.status_code not in AcceptableCodes.list():
                    raise requests.HTTPError(f"[{res.status_code}] : {res.content}")
            responses.append(res)
        return responses
