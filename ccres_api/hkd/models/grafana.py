from django.db import models

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


