from django.db import models
from typing import Union


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
