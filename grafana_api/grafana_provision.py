from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from grafana_api.models.contact import (
    GrafanaContactPointModelEmail,
    GrafanaContactPointModelEmailSettings,
)
from grafana_api.models.notification_policies import (
    GrafanaRouteModel,
    GrafanaRegexpsMatcherModel,
    GrafanaMatchType,
)
from grafana_api.models.alert import (
    ModelAlert,
    ModelAlertRule,
    ModelAlertRuleGrafanaAlertDataModel,
    ModelAlertRuleGrafanaAlert,
    ModelAlertRuleGrafanaAlertData,
    ReducerType,
    GrafanaDatasource,
    GrafanaRelativeTimeRange,
)
from query import FluxQueryBuilder
from alert_manager import GrafanaAlertManager, GrafanaAlertRuleManager
from base import GrafanaSerializer, AcceptableCodes
from pprint import pprint as print

load_dotenv("../.env.dev")

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
    alert = ModelAlert(
        interval="5m",
        name="Fast evaluated",
        rules=[
            ModelAlertRule(
                _for="5m",
                grafana_alert=ModelAlertRuleGrafanaAlert(
                    title="My alert",
                    condition="B",
                    _for="5m",
                    data=[
                        ModelAlertRuleGrafanaAlertData(
                            refId="A",
                            datasourceUid="ChyluIf4k",
                            model=ModelAlertRuleGrafanaAlertDataModel(
                                intervalMs=300000,
                                query='from(bucket: "test")\n'
                                "  |> range(start: -1h)\n"
                                '  |> filter(fn: (r) => r._measurement ==  "go_goroutines")',
                            ),
                            relativeTimeRange=GrafanaRelativeTimeRange(300, 0),
                        ),
                        ModelAlertRuleGrafanaAlertData(
                            refId="B",
                            datasourceUid="__expr__",
                            model=ModelAlertRuleGrafanaAlertDataModel(
                                GrafanaDatasource("__expr__", "__expr__"),
                                intervalMs=300000,
                                query="",
                                type="reduce",
                                reducer=ReducerType.MAX.value,
                                expression="A",
                            ),
                            relativeTimeRange=GrafanaRelativeTimeRange(0, 0),
                        ),
                    ],
                ),
            )
        ],
    )

    alert_rule_manager = GrafanaAlertRuleManager(GRAFANA_API_URL, session)
    alert_rule_manager.add_alert(alert)
    alert_rule_manager.push()


if __name__ == "__main__":

    main()
