from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Operator(models.TextChoices):
    """Classic mathematical operator for CharField"""

    GREATER = "gt", ">"
    GREATER_EQUAL = "gte", ">="
    LOWER = "lt", "<"
    LOWER_EQUAL = "lte", "<="
    EQUAL = "eq", "=="
    NOT_EQUAL = "neq", "=="


class BoolOperator(models.TextChoices):
    """Boolean operator for CharField"""

    BOOL_AND = "bool_and", "AND"
    BOOL_OR = "bool_or", "OR"
    BOOL_NOT = "bool_not", "NOT"


class DurationUnit(models.TextChoices):
    """Unit of duration for CharField"""

    YEAR = "year", "year"
    DAY = "day", "day"
    HOUR = "hour", "hour"
    MINUTE = "minute", "minute"
    SECOND = "second", "second"


class MessageLevel(models.TextChoices):
    """Message level for CharField"""

    INFO = "info", "info"
    WARNING = "warning", "warning"
    ERROR = "error", "error"
    CRITICAL = "critical", "critical"


class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()

    class Meta:
        verbose_name = "Station"


class InstrumentModel(models.Model):
    """Model of the instrument

    For example CHM15K or BASTA
    """

    model = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=1000)
    principal_investigator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Model of an instrument"


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Category of an instrument"


class Instrument(models.Model):
    pid = models.URLField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    is_active = models.BooleanField()
    instrument_type = models.ForeignKey(InstrumentModel, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(InstrumentCategory, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Instrument of station"


class Firmware(models.Model):
    version = models.CharField(max_length=100)
    condition = models.CharField(max_length=3, choices=Operator.choices, blank=True)
    instrument_model = models.ForeignKey(InstrumentModel, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Firmware information"


class Grafana(models.Model):
    url = models.CharField(max_length=100)
    port = models.IntegerField()
    version = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Grafana information"


class GrafanaDashboard(models.Model):
    name = models.CharField(max_length=100)
    content = models.JSONField()
    source = models.CharField(max_length=100, blank=True)
    grafana = models.ForeignKey(Grafana, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Grafana dashboard information"


class GrafanaPanel(models.Model):
    name = models.CharField(max_length=100)
    content = models.JSONField()
    dashboard = models.ForeignKey(GrafanaDashboard, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Grafana panel information"


class Influx(models.Model):
    url = models.CharField(max_length=100)
    port = models.IntegerField()
    version = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Influx information"


class InfluxSource(models.Model):
    bucket = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    measurement = models.CharField(max_length=100)
    influx = models.ForeignKey(Influx, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Influx source information"


class Parameter(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    variable_in_file = models.CharField(max_length=100, blank=True)
    file_type = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    instrument_model = models.ForeignKey(InstrumentModel, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Parameter information"


class Preprocessing(models.Model):
    description = models.TextField()
    reference = models.CharField(max_length=100)
    required = models.BooleanField()
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Preprocessing of parameter to apply"


class AlertContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Contact for alerting"
        unique_together = ("name", "email")


class Alert(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(AlertContact, on_delete=models.DO_NOTHING)
    evaluation_duration = models.FloatField()
    evaluation_duration_unit = models.CharField(max_length=10, choices=DurationUnit.choices)
    evaluation_processing = models.CharField(max_length=100)
    evaluation_frequency = models.IntegerField()
    evaluation_frequency_unit = models.CharField(max_length=10, choices=DurationUnit.choices)
    message_summary = models.CharField(max_length=100)
    message_description = models.CharField(max_length=1000)
    message_level = models.CharField(max_length=10, choices=MessageLevel.choices)
    trigger_minimum = models.FloatField()
    trigger_maximum = models.FloatField()
    trigger_condition = models.CharField(max_length=10, choices=Operator.choices)
    trigger_condition_value = models.FloatField()
    trigger_value = models.FloatField()
    trigger_duration = models.FloatField()
    trigger_duration_unit = models.CharField(max_length=10, choices=DurationUnit.choices)

    class Meta:
        verbose_name = "Alert of parameter information"


class AlertDependency(models.Model):
    alert_left = models.ForeignKey(Alert, related_name="alert_left", on_delete=models.DO_NOTHING)
    alert_right = models.ForeignKey(Alert, related_name="alert_right", on_delete=models.DO_NOTHING)
    condition = models.CharField(max_length=10, choices=BoolOperator.choices, blank=True)

    class Meta:
        verbose_name = "Dependency between alerts"
