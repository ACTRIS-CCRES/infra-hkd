"""
Signals that are run when a object is saved or updated in the db
"""
from .models import AlertContact, Parameter
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Type
from services.grafana_api.notification_manager import NotificationManager
from services.grafana_api.addons.contact import (
    ContactPointEmail,
    ContactPointEmailSettings,
)
from .sessions import get_grafana_session
from config.settings.base import (
    GRAFANA_API_URL,
)
from services.grafana_api.dashboard_manager import DashboardManager
from services.grafana_api.query import FluxQueryBuilder
from grafanalib.core import Dashboard, TimeSeries, GaugePanel, Target, GridPos, OPS_FORMAT


@receiver(post_save, sender=AlertContact)
def create_grafana_contact(sender: Type[AlertContact], instance: AlertContact, created, **kwargs):
    if not created:
        return None

    session = get_grafana_session()
    contact_point = ContactPointEmail(
        instance.name, ContactPointEmailSettings(addresses=[instance.email])
    )

    notification_manager = NotificationManager(GRAFANA_API_URL, session)
    notification_manager.add_contact_point(contact_point)
    notification_manager.push()


@receiver(post_save, sender=Parameter)
def create_grafana_contact(sender: Type[Parameter], instance: Parameter, created, **kwargs):
    """WIP: Not working as it is"""
    if not created:
        return None

    session = get_grafana_session()

    flux_query = (
        FluxQueryBuilder("My bucket")
        .range(start="5m", stop="2m")
        .filter(on="_measurement", what=instance.name)
        .build()
    )

    dashboard = Dashboard(
        title=instance.instrument_model.model,
        description=instance.instrument_model.description,
        tags=[instance.instrument_model.model],
        timezone="browser",
        panels=[
            TimeSeries(
                title=instance.name,
                dataSource="influxdb",
                targets=[
                    Target(
                        expr=flux_query,
                        legendFormat="{{ handler }}",
                        refId="A",
                    ),
                ],
                unit=OPS_FORMAT,
                gridPos=GridPos(h=8, w=16, x=0, y=10),
            ),
        ],
    ).auto_panel_ids()

    dashboard_manager = DashboardManager(GRAFANA_API_URL, session)
    dashboard_manager.add_dashboard(dashboard)
    dashboard_manager.push()
