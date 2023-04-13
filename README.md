Run with 

```
docker-compose --env-file .env.dev up
```

# Grafana API

## Add a contact point 

```python
    from addons.contact import ContactPointEmail, ContactPointEmailSettings
    from notification_manager import NotificationManager

    GRAFANA_API_URL = "http://localhost:3000/api"
    GRAFANA_AUTH = requests.auth.HTTPBasicAuth("admin", "admin")

    session = requests.Session()
    session.auth = GRAFANA_AUTH
    session.headers.update({"x-disable-provenance": "true"})

    notification_manager = NotificationManager(GRAFANA_API_URL, session)
    contact_point = ContactPointEmail(
        "New contact point", ContactPointEmailSettings(addresses=["a@c.d"])
    )

    notification_manager.add_contact_point(contact_point)
    notification_manager.push()
```

## Add a notification policy

```python
    from addons.notification_policies import Notification, RegexMatcher, GrafanaMatchType
    from notification_manager import NotificationManager

    GRAFANA_API_URL = "http://localhost:3000/api"
    GRAFANA_AUTH = requests.auth.HTTPBasicAuth("admin", "admin")

    session = requests.Session()
    session.auth = GRAFANA_AUTH
    session.headers.update({"x-disable-provenance": "true"})

    notification_manager = NotificationManager(GRAFANA_API_URL, session)

    notification_policy = Notification(
        "New contact point",
        object_matchers=[
            RegexMatcher("TEAM", GrafanaMatchType.EQUAL.value, "dev")
        ],
    )
    alert_manager.add_notification_policy(notification_policy)
    alert_manager.push()
```

## Add an alert

Adding an alert is quite tricky, It relies on the Alert models from the grafanalib package. 
Please see 
- https://github.com/weaveworks/grafanalib
- https://grafanalib.readthedocs.io/en/stable/
- 
It is much more easier to start from this example and build your own rule.

```python
    from alert_manager import AlertManager
    from addons.alert import AlertRulev9Fixed
    from grafanalib.core import (
        AlertGroup,
        Target,
        AlertCondition,
        AlertExpression,
        GreaterThan,
        OP_AND,
        RTYPE_LAST,
        EXP_TYPE_CLASSIC,
    )
    alertgroup = AlertGroup(
        name="Production Alerts",
        evaluateInterval="10m",
        # Each AlertRule forms a separate alert.
        rules=[
            # Alert rule using classic condition > 3
            AlertRulev9Fixed(
                # Each rule must have a unique title
                title="Alert for something 1",
                uid='alert1',
                # Several triggers can be used per alert
                condition='B',
                triggers=[
                    # A target refId must be assigned, and exist only once per AlertRule.
                    Target(
                        expr="from(bucket: \"sensors\")\n  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  |> filter(fn: (r) => r[\"_measurement\"] == \"remote_cpu\")\n  |> filter(fn: (r) => r[\"_field\"] == \"usage_system\")\n  |> filter(fn: (r) => r[\"cpu\"] == \"cpu-total\")\n  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)\n  |> yield(name: \"mean\")",
                        # Set datasource to name of your datasource
                        # If it does not work set the datasourceUID
                        datasource="ChyluIf4k",
                        refId="A",
                    ),
                    AlertExpression(
                        refId="B",
                        expressionType=EXP_TYPE_CLASSIC,
                        expression='A',
                        conditions=[
                            AlertCondition(
                                evaluator=GreaterThan(3),
                                operator=OP_AND,
                                reducerType=RTYPE_LAST
                            )
                        ]
                    )
                ],
                annotations={
                    "summary": "The database is down",
                    "runbook_url": "runbook-for-this-scenario.com/foo",
                },
                labels={
                    "environment": "prod",
                    "slack": "prod-alerts",
                },
                evaluateFor="3m",
            ),
        ]
    )
    GRAFANA_API_URL = "http://localhost:3000/api"
    GRAFANA_AUTH = requests.auth.HTTPBasicAuth("admin", "admin")


    session = requests.Session()
    session.auth = GRAFANA_AUTH
    session.headers.update({"x-disable-provenance": "true"})

    alert_rule_manager = AlertManager(GRAFANA_API_URL, session)
    alert_rule_manager.add_alert(alertgroup, folder="My custom folder")
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