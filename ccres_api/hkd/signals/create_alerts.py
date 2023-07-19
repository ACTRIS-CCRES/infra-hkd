"""
Signals that are run when a object is saved or updated in the db
"""
from ..models import (
    Alert,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Type
from config.settings.base import INFLUX_DB_BUCKET
from ..sessions import get_grafana_session
from config.settings.base import (
    GRAFANA_API_URL,
)
from services.grafana_api.query import FluxQueryBuilder
from grafanalib.core import Target

from services.grafana_api.alert_manager import AlertManager
from services.grafana_api.addons.alert import AlertRulev9Fixed
from grafanalib.core import (
    AlertGroup,
    Target,
    AlertCondition,
    AlertExpression,
    GreaterThan,
)

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


@receiver(post_save, sender=Alert)
def create_grafana_alert(sender: Type[Alert], instance: Alert, created, **kwargs):
    """WIP: Not working as it is"""
    if not created:
        return None

    session = get_grafana_session()
    flux_query = (
        FluxQueryBuilder("My bucket")
        .range(start="v.timeRangeStart", stop="v.timeRangeStop")
        .filter(on="_measurement", what=instance.parameter)
        .build()
    )

    alertgroup = AlertGroup(
        name="Production Alerts",
        evaluateInterval="10m",
        # Each AlertRule forms a separate alert.
        rules=[
            # Alert rule using classic condition > 3
            AlertRulev9Fixed(
                # Each rule must have a unique title
                title=instance.title,
                # uid="alert1",
                # Several triggers can be used per alert
                condition="B",
                triggers=[
                    # A target refId must be assigned, and exist only once per AlertRule.
                    Target(
                        expr=flux_query,
                        # Set datasource to name of your datasource
                        # If it does not work set the datasourceUID
                        datasource="InfluxDB",
                        refId="A",
                    ),
                    AlertExpression(
                        refId="B",
                        expressionType=EXP_TYPE_CLASSIC,
                        expression="A",
                        conditions=[
                            AlertCondition(
                                evaluator=GreaterThan(3), operator=OP_AND, reducerType=RTYPE_LAST
                            )
                        ],
                    ),
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
        ],
    )

    alert_rule_manager = AlertManager(GRAFANA_API_URL, session)
    alert_rule_manager.add_alert(alertgroup, folder="My custom folder")
    alert_rule_manager.push()
