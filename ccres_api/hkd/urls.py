from django.urls import path
from .views import (
    StationViewSet,
    InstrumentViewSet,
    GrafanaViewSet,
    GrafanaPanelViewSet,
    GrafanaDashboardViewSet,
    InfluxViewSet,
    InfluxSourceViewSet,
    ParameterViewSet,
    FirmwareViewSet,
    PreprocessingViewSet,
    AlertContactViewSet,
    AlertViewSet,
    AlertDependencyViewSet,
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"api/v1/station", StationViewSet)
router.register(r"api/v1/instrument", InstrumentViewSet)
router.register(r"api/v1/grafana", GrafanaViewSet)
router.register(r"api/v1/grafanapanel", GrafanaPanelViewSet)
router.register(r"api/v1/grafanadashboard", GrafanaDashboardViewSet)
router.register(r"api/v1/influx", InfluxViewSet)
router.register(r"api/v1/influxsource", InfluxSourceViewSet)
router.register(r"api/v1/parameter", ParameterViewSet)
router.register(r"api/v1/firmware", FirmwareViewSet)
router.register(r"api/v1/preprocessing", PreprocessingViewSet)
router.register(r"api/v1/alertcontact", AlertContactViewSet)
router.register(r"api/v1/alert", AlertViewSet)
router.register(r"api/v1/alertdependency", AlertDependencyViewSet)

urlpatterns = router.urls
