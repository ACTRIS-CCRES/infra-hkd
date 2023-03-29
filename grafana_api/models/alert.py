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
    _from: int = 300
    to: int = 0
    remove_first_underscore: List[str] = field(default_factory=lambda: ["_from"])


@dataclass
class GrafanaDatasource(GrafanaSerializer):
    type: str
    uid: Optional[str]


class EvaluatorType(str, Enum):
    GREATER_THAN = "gt"
    LOWER_THAN = "lt"
    WITHIN_RANGE = "within_range"
    OUTSIDE_RANGE = "outside_range"
    NO_VALUE = "outside_range"


class OperatorType(str, Enum):
    AND = "and"
    OR = "or"


class ReducerType(str, Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    LAST = "last"
    MEDIAN = "median"
    DIFF = "diff"
    DIFF_ABS = "diff_abs"
    PERCENT_DIFF = "percent_diff"
    PERCENT_DIFF_ABS = "percent_diff_abs"
    COUNT_NON_NULL = "count_non_null"


@dataclass
class ModelEvaluator(GrafanaSerializer):
    params: List[Any] = field(default_factory=lambda: [])
    type: str = ""


@dataclass
class ModelOperator(GrafanaSerializer):
    params: List[Any] = field(default_factory=lambda: [])
    type: str = ""


@dataclass
class ModelQuery(GrafanaSerializer):
    params: List[Any] = field(default_factory=lambda: [])
    type: str = ""


@dataclass
class ModelReducer(GrafanaSerializer):
    params: List[Any] = field(default_factory=lambda: [])
    type: str = ""


@dataclass
class ModelAlertRuleGrafanaAlertDataModelCondition(GrafanaSerializer):
    evaluator: ModelEvaluator = ModelEvaluator()
    operator: ModelOperator = ModelOperator()
    query: ModelQuery = ModelQuery()
    reducer: ModelReducer = ModelReducer()
    type: str = "query"


@dataclass
class ModelAlertRuleGrafanaAlertDataModel(GrafanaSerializer):
    """Data model of the Grafana Alert rule

    Attributes
    ----------
    datasource: Optional[GrafanaDatasource]
        Datasrouce of the query, by default None
    refId: Optional[str]
        Id of the model, by default None
    intervalMs: int
        Interval in ms , by default 300000
    maxDataPoints: int
        Max data points, by default 100
    query: Optional[str]
        Query to execute, by default None
    conditions: Optional[List[ModelAlertRuleGrafanaAlertDataModelCondition]]
        If query is __expr__ then we need to use this, by default None
    type: Optional[str]
        Type of the query, for example reduce, by default None
    expression: Optional[str]
        On which expression we use the type (reduce on A for example), by default None
    reducer: Optional[str]
        Which type of reducer, see ReducerType enum, by default None
    hide: bool
        Hide or not this model, by default False
    """

    datasource: Optional[GrafanaDatasource] = None
    refId: Optional[str] = None
    intervalMs: int = 300000
    maxDataPoints: int = 100
    query: Optional[str] = None
    conditions: Optional[List[ModelAlertRuleGrafanaAlertDataModelCondition]] = None
    type: Optional[str] = None
    expression: Optional[str] = None
    reducer: Optional[str] = None
    hide: bool = False

    def validate(self):
        if self.conditions is None and self.query is None:
            raise ValueError("You need to provide at least one of the following: conditions, query")


@dataclass
class ModelAlertRuleGrafanaAlertData(GrafanaSerializer):
    """Data of the Grafana Alert rule

    Attributes
    ----------
    refId: str
        Identifier of this alert rule, by conventions iter through alphabet in caps
        A -> B -> C and so on
    datasourceUid: str
        UID of the datasource to use
    model: ModelAlertRuleGrafanaAlertDataModel
        Model of the alert
    relativeTimeRange: GrafanaRelativeTimeRange
        Relative time range to apply
    queryType: str
        Type of the query, by default ""
    """

    refId: str
    datasourceUid: str
    model: ModelAlertRuleGrafanaAlertDataModel
    relativeTimeRange: GrafanaRelativeTimeRange = GrafanaRelativeTimeRange()
    queryType: str = ""


@dataclass
class ModelAlertRuleGrafanaAlert(GrafanaSerializer):
    """
    Annotations of the alerts

    Attributes
    ----------
    title: str
        Title of the alert
    condition: str
        Condition to choose to apply from the data conditions
    data: List[ModelAlertRuleGrafanaAlertData]
        List of the alerts rule
    _for: str
        For how long the alert is evaluated,
    no_data_state: str
        How to handle the missing data, by default "NoData"
    orgID: Optional[int]
        Organisation ID, by default None
    folderUID: Optional[str]
        Folder UID, by default None
    rule_group: Optional[str]
        Rule Group, by default None
    execErrState: str "
        What to do on error, by default "Error
    annotations: Optional[str]
        Annoations, by default None
    id: Optional[str]
        Id of the alert, by default None
    labels: Optional[Dict[str, str]]
        labels of the alert, by default None
    provenance: Optional[str]
        Provenance of the POST, by default None
    uid: Optional[str]
        UID of the alert, by default None
    updated: Optional[str]
        When it was updated, by default None
    """

    title: str
    condition: str
    data: List[ModelAlertRuleGrafanaAlertData]
    _for: str
    no_data_state: str = "NoData"
    orgID: Optional[int] = None
    folderUID: Optional[str] = None
    rule_group: Optional[str] = None
    execErrState: str = "Error"
    annotations: Optional[str] = None
    id: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    provenance: Optional[str] = None
    uid: Optional[str] = None
    updated: Optional[str] = None
    remove_first_underscore: List[str] = field(default_factory=lambda: ["_for"])


@dataclass
class GrafanaAnnotations(GrafanaSerializer):
    """
    Annotations of the alerts

    Attributes
    ----------
    __dashboardUid__ : Optional[str]
        You need to fill this parameter in order to link the alert with the dashboard
    __panelId__: Optional[str]
        You need to fill this parameter in order to link the alert with the dashboard
    __alertId__: Optional[str]
        Alert ID
    description: Optional[str]
        Description of the alert
    summary: Optional[str]
        Summary of the alert
    runbook_url: Optional[str]
        Runbook URL
    """

    __dashboardUid__: Optional[str] = None
    __panelId__: Optional[str] = None
    __alertId__: Optional[int] = None
    description: Optional[str] = None
    runbook_url: Optional[str] = None
    summary: Optional[str] = None


@dataclass
class ModelAlertRule(GrafanaSerializer):
    """
    Model for alerts of Grafana

    Attributes
    ----------
    _for : str
        Once the condition is breached, the alert goes into pending state.
        If the alert is pending longer than the _for, it becomes a firing alert.
    grafana_alert: ModelAlertRuleGrafanaAlert
        Configuration of the alert
    annotations: Optional[GrafanaAnnotations]
        Annotations of the alert. It handles things like summary, description or linking to panels
        by default None
    remove_first_underscore: List[str]
        Intern value for dataclasses, by default ["_for"]
    """

    _for: str  # noqa
    grafana_alert: ModelAlertRuleGrafanaAlert
    annotations: Optional[GrafanaAnnotations] = None
    remove_first_underscore: List[str] = field(default_factory=lambda: ["_for"])


@dataclass
class ModelAlert(GrafanaSerializer):
    """
    Model for the group of alert of Grafana

    Attributes
    ----------
    name : str
        Name of the group of the alert
    interval : str
        Interval of evaluation of the group of the alert.
        Applies to every rule within a group.
        It can overwrite the interval of an existing alert rule.
    rules : List[ModelAlertRule]
        List of alerts within the group
    labels : Optional[Dict[str, str]]
        Dictionnary of labels for the notification
    """

    name: str
    interval: str
    rules: List[ModelAlertRule]
    labels: Optional[Dict[str, str]] = None


# We need to reproduce this :


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
#                                     "hide": False,
#                                     "intervalMs": 1000,
#                                     "maxDataPoints": 43200,
#                                     "refId": "B",
#                                     "expression": "A",
#                                     "type": "reduce",
#                                     "reducer": "last",
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
