from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (
    StationSerializer,
    InfluxSerializer,
    InfluxSourceSerializer,
    InstrumentSerializer,
    GrafanaSerializer,
    GrafanaDashboardSerializer,
    GrafanaPanelSerializer,
    AlertSerializer,
    AlertContactGroupSerializer,
    AlertContactSerializer,
    AlertDependencySerializer,
    ParameterSerializer,
    PreprocessingSerializer,
    FirmwareSerializer,
)
from .models import (
    Station,
    Influx,
    InfluxSource,
    Instrument,
    Grafana,
    GrafanaDashboard,
    GrafanaPanel,
    Alert,
    AlertContactGroup,
    AlertContact,
    AlertDependency,
    Parameter,
    Preprocessing,
    Firmware,
)

# https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes
# Create your views here.


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer
    queryset = Station.objects.all()
    permission_class = [IsAuthenticated]


class InstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()
    permission_class = [IsAuthenticated]


class GrafanaViewSet(viewsets.ModelViewSet):
    serializer_class = GrafanaSerializer
    queryset = Grafana.objects.all()
    permission_class = [IsAuthenticated]


class GrafanaPanelViewSet(viewsets.ModelViewSet):
    serializer_class = GrafanaPanelSerializer
    queryset = GrafanaPanel.objects.all()
    permission_class = [IsAuthenticated]


class GrafanaDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = GrafanaDashboardSerializer
    queryset = GrafanaDashboard.objects.all()
    permission_class = [IsAuthenticated]


class InfluxViewSet(viewsets.ModelViewSet):
    serializer_class = InfluxSerializer
    queryset = Influx.objects.all()
    permission_class = [IsAuthenticated]


class InfluxSourceViewSet(viewsets.ModelViewSet):
    serializer_class = InfluxSourceSerializer
    queryset = InfluxSource.objects.all()
    permission_class = [IsAuthenticated]


class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()
    permission_class = [IsAuthenticated]


class FirmwareViewSet(viewsets.ModelViewSet):
    serializer_class = FirmwareSerializer
    queryset = Firmware.objects.all()
    permission_class = [IsAuthenticated]


class PreprocessingViewSet(viewsets.ModelViewSet):
    serializer_class = PreprocessingSerializer
    queryset = Preprocessing.objects.all()
    permission_class = [IsAuthenticated]


class AlertContactGroupViewSet(viewsets.ModelViewSet):
    serializer_class = AlertContactGroupSerializer
    queryset = AlertContactGroup.objects.all()
    permission_class = [IsAuthenticated]


class AlertContactViewSet(viewsets.ModelViewSet):
    serializer_class = AlertContactSerializer
    queryset = AlertContact.objects.all()
    permission_class = [IsAuthenticated]


class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    queryset = Alert.objects.all()
    permission_class = [IsAuthenticated]


class AlertDependencyViewSet(viewsets.ModelViewSet):
    serializer_class = AlertDependencySerializer
    queryset = AlertDependency.objects.all()
    permission_class = [IsAuthenticated]
