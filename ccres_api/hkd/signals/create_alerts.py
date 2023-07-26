"""
Signals that are run when a object is saved or updated in the db
"""
from typing import Any, Dict, List, Optional, Type

from config.settings.base import (
    GRAFANA_ALERTS_FOLDER,
    GRAFANA_API_URL,
    INFLUX_DB_BUCKET,
    INFLUX_DB_DATASOURCE_NAME,
)
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from grafanalib.core import (
    EXP_TYPE_CLASSIC,
    OP_AND,
    RTYPE_LAST,
    AlertCondition,
    AlertExpression,
    AlertGroup,
    GreaterThan,
    LowerThan,
    NoValue,
    OutsideRange,
    Target,
    WithinRange,
)
from hkd.models import Alert, Instrument, Station
from hkd.models.helpers import DurationUnit, Operator
from hkd.sessions import get_grafana_session
from services.grafana_api.addons.alert import AlertRulev9Fixed
from services.grafana_api.alert_manager import AlertManager
from services.grafana_api.datasources_manager import DatasourceManager
from services.grafana_api.query import FluxQueryBuilder


def _get_uid_of_datasource(datasource_name: str, folder_json: Dict[Any, Any]) -> Optional[str]:
    for sub_json in folder_json:
        title = sub_json.get("name")
        if title is not None and title == datasource_name:
            return sub_json.get("uid")


def create_conditions(instance: Alert) -> List[AlertCondition]:
    """Create conditions for the alerts based on the alert instance

    Parameters
    ----------
    instance : Alert
        Object of the Alert model

    Returns
    -------
    List[AlertCondition]
        List of alert conditions
    """
    conditions = []
    triggers = [
        (instance.trigger_minimum, instance.trigger_minimum_condition),
        (instance.trigger_maximum, instance.trigger_maximum_condition),
    ]
    for value, condition in triggers:
        if not (value and condition):
            continue

        if condition == Operator.GREATER or condition == Operator.GREATER_EQUAL:
            alert_condition = AlertCondition(
                evaluator=GreaterThan(value),
                operator=OP_AND,
                reducerType=instance.evaluation_method,
            )
        elif condition == Operator.LOWER or condition == Operator.LOWER_EQUAL:
            alert_condition = AlertCondition(
                evaluator=LowerThan(value),
                operator=OP_AND,
                reducerType=instance.evaluation_method,
            )
        elif condition == Operator.NOT_EQUAL:
            alert_condition = AlertCondition(
                evaluator=OutsideRange(value, value),
                operator=OP_AND,
                reducerType=instance.evaluation_method,
            )
        elif condition == Operator.EQUAL:
            alert_condition = AlertCondition(
                evaluator=WithinRange(value, value),
                operator=OP_AND,
                reducerType=instance.evaluation_method,
            )
        conditions.append(alert_condition)
    return conditions


def get_alert_group(datasource_uid, alert, parameter, instrument_model, station, contact_group):
    flux_query = (
        FluxQueryBuilder(INFLUX_DB_BUCKET)
        .range(start="v.timeRangeStart", stop="v.timeRangeStop")
        .filter(on="_measurement", what=instrument_model.model)
        .filter(on="_field", what=parameter.name)
        .filter(on="site", what=station.name)
        .build()
    )
    evaluation_frequency_seconds = DurationUnit.to_seconds(
        alert.evaluation_frequency_unit, alert.evaluation_frequency
    )
    evaluation_duration_seconds = DurationUnit.to_seconds(
        alert.evaluation_duration_unit, alert.evaluation_duration
    )
    conditions = create_conditions(alert)

    alertgroup = AlertGroup(
        name=station.name,
        evaluateInterval=f"{evaluation_frequency_seconds}s",
        rules=[
            AlertRulev9Fixed(
                title=alert.title,
                condition="B",
                triggers=[
                    Target(
                        refId="A",
                        datasource=datasource_uid,
                        expr=flux_query,
                    ),
                    AlertExpression(
                        refId="B",
                        expressionType=EXP_TYPE_CLASSIC,
                        expression="A",
                        conditions=conditions,
                    ),
                ],
                annotations={
                    "summary": alert.message_summary,
                    "description": alert.message_description,
                },
                labels={
                    "team": contact_group.name,
                },
                evaluateFor=f"{evaluation_duration_seconds}s",
            ),
        ],
    )

    return alertgroup


@receiver(post_save, sender=Alert)
@receiver(post_delete, sender=Alert)
def create_grafana_alert(sender: Type[Alert], instance: Alert, **kwargs):
    session = get_grafana_session()
    alert_rule_manager = AlertManager(GRAFANA_API_URL, session)
    datasource_manager = DatasourceManager(GRAFANA_API_URL, session)
    datasource_uid = _get_uid_of_datasource(
        INFLUX_DB_DATASOURCE_NAME, datasource_manager.get_fetched_json()
    )
    alerts = Alert.objects.all()

    # If no alerts remove all the folders
    if len(alerts) == 0:
        alert_rule_manager.delete_folder(GRAFANA_ALERTS_FOLDER)

    for alert in alerts:
        parameter = alert.parameter
        instrument_model = parameter.instrument_model

        stations = Station.objects.filter(instrument__instrument_model=instrument_model)

        for station in stations:
            instruments = Instrument.objects.filter(instrument_model=instrument_model)
            for instrument in instruments:
                contact_group = instrument.contact_group
                alertgroup = get_alert_group(
                    datasource_uid, alert, parameter, instrument_model, station, contact_group
                )
                alert_rule_manager.add_alert(alertgroup, folder=GRAFANA_ALERTS_FOLDER)
    alert_rule_manager.push(delete_existing=True)
