from django.db import models
from hkd.models.instrument import InstrumentModel


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
