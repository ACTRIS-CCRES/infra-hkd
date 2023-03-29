Run with 

```
docker-compose --env-file .env.dev up
```

# Grafana API

## Add a contact point 

```python
from contact import GrafanaContactPointModelEmail, GrafanaContactPointModelEmailSettings
from alert_manager import GrafanaAlertManager

GRAFANA_API_URL = "http://localhost:3000/api"
GRAFANA_AUTH = requests.auth.HTTPBasicAuth("admin", "admin")

session = requests.Session()
session.auth = GRAFANA_AUTH
session.headers.update({"x-disable-provenance": "true"})

alert_manager = GrafanaAlertManager(GRAFANA_API_URL, session)
contact_point = GrafanaContactPointModelEmail(
    "New contact point", GrafanaContactPointModelEmailSettings(addresses=["a@c.d"])
)

alert_manager.add_contact_point(contact_point)
alert_manager.push()
```

## Add a notification policy

```python
from notification_policies import GrafanaRouteModel, GrafanaRegexpsMatcherModel, GrafanaMatchType
from alert_manager import GrafanaAlertManager

GRAFANA_API_URL = "http://localhost:3000/api"
GRAFANA_AUTH = requests.auth.HTTPBasicAuth("admin", "admin")

session = requests.Session()
session.auth = GRAFANA_AUTH
session.headers.update({"x-disable-provenance": "true"})

alert_manager = GrafanaAlertManager(GRAFANA_API_URL, session)

notification_policy = GrafanaRouteModel(
    "New contact point",
    object_matchers=[
        GrafanaRegexpsMatcherModel("TEAM", GrafanaMatchType.EQUAL.value, "dev")
    ],
)
alert_manager.add_notification_policy(notification_policy)
alert_manager.push()
```

## Add an alert

Adding an alert is really tricky, the most part of the models appears sometimes to not be used at all. 
It is much more easier to start from this example and build your own rule.

```python
from alert_manager import GrafanaAlertRuleManager
from alert import (
    ModelAlert,
    ModelAlertRule,
    ModelAlertRuleGrafanaAlertDataModel,
    ModelAlertRuleGrafanaAlert,
    ModelAlertRuleGrafanaAlertData,
    ReducerType,
    GrafanaDatasource,
    GrafanaRelativeTimeRange,
)
GRAFANA_API_URL = "http://localhost:3000/api"
GRAFANA_AUTH = requests.auth.HTTPBasicAuth("admin", "admin")

session = requests.Session()
session.auth = GRAFANA_AUTH
session.headers.update({"x-disable-provenance": "true"})


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

```

## Build a flux query 

```python
query = (
    FluxQueryBuilder("My bucket")
    .range(start="5m", stop="2m")
    .filter(on="_measurement", what="my_var")
    .build()
)
print(query)
```
will print 

```
from(bucket: "My bucket")
    |> range(start: 5m , stop: 2m)
    |> filter(fn: (r) => r["_measurement"] == "my_var")
```