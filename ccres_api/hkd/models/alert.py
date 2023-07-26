from django.db import models
from django.core.exceptions import ValidationError
from hkd.models.helpers import DurationUnit, EvaluateMethod, MessageLevel, Operator, BoolOperator
from hkd.models.parameter import Parameter


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
            msg = (
                "Either trigger_minimum and trigger_minimum_condition,"
                " or trigger_maximum and trigger_maximum_condition,"
                " or both must be provided together."
            )
            errors["trigger_minimum"] = msg
            errors["trigger_minimum_condition"] = msg
            errors["trigger_maximum"] = msg
            errors["trigger_maximum_condition"] = msg
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
