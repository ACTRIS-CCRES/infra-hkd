from rest_framework import serializers
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


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = "__all__"


class GrafanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grafana
        fields = "__all__"


class GrafanaPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrafanaPanel
        fields = "__all__"


class GrafanaDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrafanaDashboard
        fields = "__all__"


class InfluxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influx
        fields = "__all__"


class InfluxSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluxSource
        fields = "__all__"


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = "__all__"


class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = "__all__"


class PreprocessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preprocessing
        fields = "__all__"


class AlertContactGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertContactGroup
        fields = "__all__"


class AlertContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertContact
        fields = "__all__"


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"


class AlertDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertDependency
        fields = "__all__"
