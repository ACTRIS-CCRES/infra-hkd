from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from base import GrafanaSerializer, AcceptableCodes
from contact import GrafanaContactPointModelEmail, GrafanaContactPointModelEmailSettings
from notification_policies import GrafanaRouteModel


class GrafanaAlertManager:

    # https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#notification-policies
    # POST /api/v1/provisioning/contact-point
    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/alertmanager/grafana/config/api/v1/alerts"
        self.config = self.session.get(self.endpoint).json()

    def add_contact_point(
        self, contact_point: GrafanaContactPointModelEmail
    ) -> "GrafanaAlertManager":
        name = contact_point.name
        contact_dict = contact_point.serialize()

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
        notification_dict = notification_policy.serialize()
        self.config["alertmanager_config"]["route"]["routes"].append(notification_dict)
        return self

    def commit(self) -> requests.Response:
        res = self.session.post(self.endpoint, json=self.config)
        return res


class GrafanaAlertRuleManager:

    # https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#notification-policies
    # POST /api/v1/provisioning/contact-point
    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/ruler/grafana/api/v1/rules"
        self.config = self.session.get(self.endpoint).json()
        from pprint import pprint as print

        print(self.config)
        exit()
