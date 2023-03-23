from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from contact import GrafanaContactPointModelEmail, GrafanaContactPointModelEmailSettings
from notification_policies import GrafanaRouteModel, GrafanaRegexpsMatcherModel, GrafanaMatchType
from alert_manager import GrafanaAlertManager, GrafanaAlertRuleManager
from base import GrafanaSerializer, AcceptableCodes

load_dotenv("../env.dev")

GRAFANA_API_URL = "http://localhost:3000/api"
GRAFANA_AUTH = requests.auth.HTTPBasicAuth(
    os.environ.get("GRAFANA_USERNAME"), os.environ.get("GRAFANA_PASSWORD")
)

# One folder per station
# One dashboard per instrument
# One panel per variable


def get_session() -> requests.Session:
    session = requests.Session()
    session.auth = GRAFANA_AUTH
    session.headers.update({"x-disable-provenance": "true"})
    return session


def main():
    session = get_session()

    alert_manager = GrafanaAlertManager(GRAFANA_API_URL, session)
    contact_point = GrafanaContactPointModelEmail(
        "Antoine From new API", GrafanaContactPointModelEmailSettings(addresses=["a@c.d"])
    )
    notification_policy = GrafanaRouteModel(
        "Antoine From new API",
        object_matchers=[
            GrafanaRegexpsMatcherModel("STATION", GrafanaMatchType.EQUAL.value, "sirta")
        ],
    )
    alert_manager.add_contact_point(contact_point)
    alert_manager.add_notification_policy(notification_policy)
    res = alert_manager.commit()
    alert_rule_manager = GrafanaAlertRuleManager(GRAFANA_API_URL, session)


if __name__ == "__main__":

    main()
