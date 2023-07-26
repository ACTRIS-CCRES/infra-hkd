from django.db import models


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
