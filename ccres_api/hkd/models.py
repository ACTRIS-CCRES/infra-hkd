from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import uuid

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

    def __str__(self):
        return f"{self.name}"


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

    def __str__(self):
        return f"{self.model}"


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Category of an instrument"

    def __str__(self):
        return f"{self.name}"


class Instrument(models.Model):
    pid = models.URLField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    is_active = models.BooleanField()
    instrument_model = models.ForeignKey(InstrumentModel, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(InstrumentCategory, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Instrument of station"

    def __str__(self):
        return f"{self.instrument_model.model} - {self.station.name} - {self.category.name}"


class Firmware(models.Model):
    version = models.CharField(max_length=100)
    condition = models.CharField(max_length=3, choices=Operator.choices, blank=True)
    instrument_model = models.ForeignKey(InstrumentModel, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Firmware information"

    def __str__(self):
        return f"{self.instrument_model.model}  {self.category.version}"


class Grafana(models.Model):
    url = models.CharField(max_length=100)
    port = models.IntegerField()
    version = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Grafana information"

    def __str__(self):
        return f"Grafana {self.version} - {self.url}"


class GrafanaDashboard(models.Model):
    name = models.CharField(max_length=100)
    content = models.JSONField()
    source = models.CharField(max_length=100, blank=True)
    grafana = models.ForeignKey(Grafana, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Grafana dashboard information"

    def __str__(self):
        return f"{self.name}"


class GrafanaPanel(models.Model):
    name = models.CharField(max_length=100)
    content = models.JSONField()
    dashboard = models.ForeignKey(GrafanaDashboard, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Grafana panel information"

    def __str__(self):
        return f"{self.name}"


class Influx(models.Model):
    url = models.CharField(max_length=100)
    port = models.IntegerField()
    version = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Influx information"

    def __str__(self):
        return f"InfluxDB {self.version}"


class InfluxSource(models.Model):
    bucket = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    measurement = models.CharField(max_length=100)
    influx = models.ForeignKey(Influx, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Influx source information"

    def __str__(self):
        return f"Bucket {self.bucket} - {self.influx.version}"


class Parameter(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    variable_in_file = models.CharField(max_length=100, blank=True)
    file_type = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=1000, blank=True)
    instrument_model = models.ForeignKey(InstrumentModel, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Parameter information"

    def __str__(self):
        return f"{self.name} - {self.instrument_model.model}"


class Preprocessing(models.Model):
    description = models.TextField()
    reference = models.CharField(max_length=100)
    required = models.BooleanField()
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Preprocessing of parameter to apply"


class AlertContactGroup(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = "Group of contact for alerting"

    def __str__(self):
        return f"{self.name}"


class AlertContact(models.Model):
    name = models.TextField()
    email = models.TextField()
    group = models.ForeignKey(AlertContactGroup, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Contact for alerting"
        unique_together = ("name", "email")

    def __str__(self):
        return f"{self.name}"


class Alert(models.Model):
    title = models.CharField(max_length=100)
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)
    contact_group = models.ForeignKey(AlertContactGroup, on_delete=models.DO_NOTHING)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class AlertDependency(models.Model):
    alert_left = models.ForeignKey(Alert, related_name="alert_left", on_delete=models.DO_NOTHING)
    alert_right = models.ForeignKey(Alert, related_name="alert_right", on_delete=models.DO_NOTHING)
    condition = models.CharField(max_length=10, choices=BoolOperator.choices, blank=True)

    class Meta:
        verbose_name = "Dependency between alerts"
