from typing import Iterable, Optional, Union
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import uuid
from django.core.exceptions import ValidationError

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


class EvaluateMethod(models.TextChoices):
    """Evaluate method for CharField"""

    AVG = "avg", "avg"
    MIN = "min", "min"
    MAX = "max", "max"
    SUM = "sum", "sum"
    COUNT = "count", "count"
    LAST = "last", "last"
    MEDIAN = "median", "median"
    DIFF = "diff", "diff"
    PERCENT_DIFF = "percent_diff", "percent_diff"
    COUNT_NON_NULL = "count_non_null", "count_non_null"


class DurationUnit(models.TextChoices):
    """Unit of duration for CharField"""

    YEAR = "year", "year"
    DAY = "day", "day"
    HOUR = "hour", "hour"
    MINUTE = "minute", "minute"
    SECOND = "second", "second"

    @staticmethod
    def to_seconds(unit: str, value: Union[float, int]) -> int:
        """
        https://github.com/grafana/grafana/blob/ac445a25d5a9492414358eb132dc8cd33b5ca209/pkg/services/alerting/rule.go#L17
        """
        if unit == "minute":
            value = float(value) * 60
        elif unit == "hour":
            value = 60 * 60
        elif unit == "day":
            value = 60 * 60 * 24
        elif unit == "year":
            value = 60 * 60 * 24 * 365
        return int(value)


class MessageLevel(models.TextChoices):
    """Message level for CharField"""

    INFO = "info", "info"
    WARNING = "warning", "warning"
    ERROR = "error", "error"
    CRITICAL = "critical", "critical"


class AlertContactGroup(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = "Group of contact for alerting"

    def __str__(self):
        return f"{self.name}"


class AlertContact(models.Model):
    name = models.TextField()
    email = models.TextField()
    groups = models.ManyToManyField(AlertContactGroup)

    class Meta:
        verbose_name = "Contact for alerting"
        unique_together = ("name", "email")

    def __str__(self):
        return f"{self.name}"


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
    contact_group = models.ForeignKey(AlertContactGroup, on_delete=models.DO_NOTHING)

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


class Alert(models.Model):
    title = models.CharField(max_length=100)
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)
    evaluation_method = models.CharField(
        max_length=30, choices=EvaluateMethod.choices, default=EvaluateMethod.LAST
    )
    evaluation_duration = models.FloatField(default=10.0)
    evaluation_duration_unit = models.CharField(
        max_length=10, choices=DurationUnit.choices, default=DurationUnit.MINUTE
    )
    evaluation_processing = models.CharField(max_length=100, blank=True)
    evaluation_frequency = models.FloatField(default=10)
    evaluation_frequency_unit = models.CharField(
        max_length=10, choices=DurationUnit.choices, default=DurationUnit.MINUTE
    )
    message_summary = models.CharField(max_length=100)
    message_description = models.CharField(max_length=1000)
    message_level = models.CharField(
        max_length=10, choices=MessageLevel.choices, default=MessageLevel.ERROR
    )
    trigger_minimum = models.FloatField(blank=True, null=True)
    trigger_minimum_condition = models.CharField(
        max_length=10, choices=Operator.choices, blank=True, null=True
    )
    trigger_maximum = models.FloatField(blank=True, null=True)
    trigger_maximum_condition = models.CharField(
        max_length=10, choices=Operator.choices, blank=True, null=True
    )
    trigger_duration = models.FloatField(default=30)
    trigger_duration_unit = models.CharField(
        max_length=10, choices=DurationUnit.choices, default=DurationUnit.MINUTE
    )

    class Meta:
        verbose_name = "Alert of parameter information"

    def clean(self):
        minimum_conditions = [self.trigger_minimum, self.trigger_minimum_condition]
        maximum_conditions = [self.trigger_maximum, self.trigger_maximum_condition]
        errors = {}
        if not any(minimum_conditions) and not any(maximum_conditions):
            errors["trigger"] = (
                "Either trigger_minimum and trigger_minimum_condition,"
                " or trigger_maximum and trigger_maximum_condition,"
                " or both must be provided together."
            )
            raise ValidationError(errors)
        if any(minimum_conditions) and not all(minimum_conditions):
            msg = "Both trigger_minimum and trigger_minimum_condition must be provided together."
            errors["trigger_minimum"] = msg
            errors["trigger_minimum_condition"] = msg
        if any(maximum_conditions) and not all(maximum_conditions):
            msg = "Both trigger_maximum and trigger_maximum_condition must be provided together."
            errors["trigger_maximum"] = msg
            errors["trigger_maximum_condition"] = msg
        if errors:
            raise ValidationError(errors)


class AlertDependency(models.Model):
    alert_left = models.ForeignKey(Alert, related_name="alert_left", on_delete=models.DO_NOTHING)
    alert_right = models.ForeignKey(Alert, related_name="alert_right", on_delete=models.DO_NOTHING)
    condition = models.CharField(max_length=10, choices=BoolOperator.choices, blank=True)

    class Meta:
        verbose_name = "Dependency between alerts"
