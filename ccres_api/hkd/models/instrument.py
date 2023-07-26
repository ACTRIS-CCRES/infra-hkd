from django.db import models
from django.contrib.auth import get_user_model

from hkd.models.helpers import Operator
from hkd.models.contact import AlertContactGroup

User = get_user_model()


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
