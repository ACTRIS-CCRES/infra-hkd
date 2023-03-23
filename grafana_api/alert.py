from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from base import GrafanaSerializer, AcceptableCodes


class GrafanaDuration:
    def __init__(self, seconds: int):
        self.seconds = seconds

    @classmethod
    def from_seconds(cls, seconds: int) -> int:
        return cls(seconds)


@dataclass
class GrafanaRelativeTimeRange(GrafanaSerializer):
    _from: int
    to: int
    remove_first_underscore: List[str] = field(default_factory=lambda: ["_from"])


@dataclass
class GrafanaDatasource(GrafanaSerializer):
    type: str
    uid: Optional[str]


@dataclass
class GrafanaAlertModelAlertQueryModel(GrafanaSerializer):
    Grafana: GrafanaDatasource
    query: str
    hide: bool = False
    intervalMs: int = 300000
    maxDataPoints: int = 100
    refId: Optional[str] = None


@dataclass
class GrafanaAlertModelAlertQuery(GrafanaSerializer):
    # Identifier of the alert
    refId: str
    model: GrafanaAlertModelAlertQueryModel
    relativeTimeRange: GrafanaRelativeTimeRange
    queryType: str = ""
    datasourceUid: Optional[str] = None


@dataclass
class GrafanaAlertModel(GrafanaSerializer):
    # Name of the condition
    condition: str
    data: List[GrafanaAlertModelAlertQuery]
    execErrState: str
    folderUID: str
    _for: str  # noqa
    noDataState: str
    org_ID: int
    ruleGroup: str
    title: str
    annotations: Optional[str]
    id: Optional[str]
    labels: Optional[Dict[str, str]]
    provenance: Optional[str]
    uid: Optional[str]
    updated: Optional[str]
    remove_first_underscore: List[str] = field(default_factory=lambda: ["_for"])


@dataclass
class GrafanaAnnotations(GrafanaSerializer):
    # Name of the condition
    __dashboardUid__: str
    __panelId__: str


@dataclass
class GrafanaAlertRuleModel(GrafanaSerializer):
    # Name of the condition
    annotations: GrafanaAnnotations
    execErrState: str


# {
#     "Alerts": [
#         {
#             "interval": "5m",
#             "name": "5 minutes",
#             "rules": [
#                 {
#                     "annotations": {"__dashboardUid__": "Xmhb9If4z", "__panelId__": "2"},
#                     "expr": "",
#                     "for": "5m",
#                     "grafana_alert": {
#                         "condition": "C",
#                         "data": [
#                             {
#                                 "datasourceUid": "ChyluIf4k",
#                                 "model": {
#                                     "datasource": {"type": "influxdb", "uid": "ChyluIf4k"},
#                                     "hide": False,
#                                     "intervalMs": 300000,
#                                     "maxDataPoints": 100,
#                                     "query": "from(bucket: "
#                                     '"test")\n'
#                                     "  |> "
#                                     "range(start: "
#                                     "-1h)\n"
#                                     "  |> "
#                                     "filter(fn: "
#                                     "(r) => "
#                                     "r._measurement "
#                                     "== "
#                                     '"go_goroutines")',
#                                     "refId": "A",
#                                 },
#                                 "queryType": "",
#                                 "refId": "A",
#                                 "relativeTimeRange": {"from": 300, "to": 0},
#                             },
#                             {
#                                 "datasourceUid": "__expr__",
#                                 "model": {
#                                     "conditions": [
#                                         {
#                                             "evaluator": {"params": [], "type": "gt"},
#                                             "operator": {"type": "and"},
#                                             "query": {"params": ["B"]},
#                                             "reducer": {"params": [], "type": "last"},
#                                             "type": "query",
#                                         }
#                                     ],
#                                     "datasource": {"type": "__expr__", "uid": "__expr__"},
#                                     "expression": "A",
#                                     "hide": False,
#                                     "intervalMs": 1000,
#                                     "maxDataPoints": 43200,
#                                     "reducer": "last",
#                                     "refId": "B",
#                                     "type": "reduce",
#                                 },
#                                 "queryType": "",
#                                 "refId": "B",
#                                 "relativeTimeRange": {"from": 300, "to": 0},
#                             },
#                             {
#                                 "datasourceUid": "__expr__",
#                                 "model": {
#                                     "conditions": [
#                                         {
#                                             "evaluator": {"params": [1250], "type": "gt"},
#                                             "operator": {"type": "and"},
#                                             "query": {"params": ["C"]},
#                                             "reducer": {"params": [], "type": "last"},
#                                             "type": "query",
#                                         }
#                                     ],
#                                     "datasource": {"type": "__expr__", "uid": "__expr__"},
#                                     "expression": "B",
#                                     "hide": False,
#                                     "intervalMs": 1000,
#                                     "maxDataPoints": 43200,
#                                     "refId": "C",
#                                     "type": "threshold",
#                                 },
#                                 "queryType": "",
#                                 "refId": "C",
#                                 "relativeTimeRange": {"from": 300, "to": 0},
#                             },
#                         ],
#                         "exec_err_state": "Error",
#                         "id": 1,
#                         "intervalSeconds": 300,
#                         "is_paused": False,
#                         "namespace_id": 2,
#                         "namespace_uid": "TBnGuvf4k",
#                         "no_data_state": "NoData",
#                         "orgId": 1,
#                         "rule_group": "5 minutes",
#                         "title": "Panel Title",
#                         "uid": "uRV7uvB4k",
#                         "updated": "2023-03-23T16:13:46Z",
#                         "version": 8,
#                     },
#                     "labels": {"STATION": "sirta"},
#                 }
#             ],
#         }
#     ]
# }
