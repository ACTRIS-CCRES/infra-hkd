"""
Signals that are run when a object is saved or updated in the db
"""
from ..models import (
    Parameter,
    Station,
    InstrumentModel,
    Instrument,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from services.grafana_api.addons.folder import Folder
from config.settings.base import INFLUX_DB_BUCKET
from ..sessions import get_grafana_session
from config.settings.base import (
    GRAFANA_API_URL,
)
from services.grafana_api.dashboard_manager import DashboardManager
from services.grafana_api.folder_manager import FolderManager
from services.grafana_api.query import FluxQueryBuilder
from grafanalib.core import Dashboard, TimeSeries, Target, GridPos

from grafanalib.core import (
    Target,
)
from typing import Dict, Optional, Any

from grafanalib.core import (
    Target,
)


def _get_uid_of_station(station_name: str, folder_json: Dict[Any, Any]) -> Optional[str]:
    for sub_json in folder_json:
        title = sub_json.get("title")
        if title is not None and title == station_name:
            return sub_json.get("uid")


def create_folders(folder_manager, stations):
    for station in stations:
        folder = Folder(station.name)
        folder_manager.add_folder(folder)
    folder_manager.push()


def build_panels(station, instrument_model, parameters):
    panels = []
    for parameter in parameters:
        flux_query = (
            FluxQueryBuilder(INFLUX_DB_BUCKET)
            .range(start="v.timeRangeStart", stop="v.timeRangeStop")
            .filter(on="_measurement", what=instrument_model.model)
            .filter(on="_field", what=parameter.name)
            .filter(on="site", what=station.name)
            .build()
        )

        panels.append(
            TimeSeries(
                title=f"{parameter.name} [{parameter.unit}]",
                dataSource="default",
                targets=[
                    Target(
                        expr=flux_query,
                        datasource="InfluxDB",
                    ),
                ],
                gridPos=GridPos(h=8, w=16, x=0, y=0),
            ),
        )

    return panels


def add_dashboards(dashboard_manager, folder_json, stations):
    for station in stations:
        station_uid = _get_uid_of_station(station.name, folder_json)

        instrument_models = InstrumentModel.objects.filter(instrument__station=station)
        for instrument_model in instrument_models:
            parameters = Parameter.objects.filter(instrument_model=instrument_model)
            panels = build_panels(station, instrument_model, parameters)

            dashboard = Dashboard(
                title=instrument_model.model,
                description=instrument_model.description,
                tags=[instrument_model.model],
                timezone="browser",
                panels=panels,
            ).auto_panel_ids()

            dashboard_manager.add_dashboard(dashboard, folder_uid=station_uid)
    dashboard_manager.push()


@receiver(post_save, sender=Station)
@receiver(post_save, sender=Instrument)
@receiver(post_save, sender=InstrumentModel)
@receiver(post_save, sender=Parameter)
def create_grafana_dashboards(sender: Any, instance: Any, created, **kwargs):
    if not created:
        return None

    session = get_grafana_session()
    dashboard_manager = DashboardManager(GRAFANA_API_URL, session)
    folder_manager = FolderManager(GRAFANA_API_URL, session)

    stations = Station.objects.all()

    create_folders(folder_manager, stations)

    folder_json = folder_manager.fetch()

    add_dashboards(dashboard_manager, folder_json, stations)
