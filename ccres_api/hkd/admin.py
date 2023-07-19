from django.contrib import admin
from .models import (
    Station,
    Influx,
    InfluxSource,
    Instrument,
    InstrumentModel,
    InstrumentCategory,
    Grafana,
    GrafanaDashboard,
    GrafanaPanel,
    Alert,
    AlertContact,
    AlertContactGroup,
    AlertDependency,
    Parameter,
    Preprocessing,
    Firmware,
)

# Register your models here.


class StationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Station, StationAdmin)


class InstrumentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Instrument, InstrumentAdmin)


class InstrumentModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(InstrumentModel, InstrumentModelAdmin)


class InstrumentCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(InstrumentCategory, InstrumentCategoryAdmin)


class GrafanaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Grafana, GrafanaAdmin)


class GrafanaPanelAdmin(admin.ModelAdmin):
    pass


admin.site.register(GrafanaPanel, GrafanaPanelAdmin)


class GrafanaDashboardAdmin(admin.ModelAdmin):
    pass


admin.site.register(GrafanaDashboard, GrafanaDashboardAdmin)


class InfluxAdmin(admin.ModelAdmin):
    pass


admin.site.register(Influx, InfluxAdmin)


class InfluxSourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(InfluxSource, InfluxSourceAdmin)


class ParameterAdmin(admin.ModelAdmin):
    pass


admin.site.register(Parameter, ParameterAdmin)


class FirmwareAdmin(admin.ModelAdmin):
    pass


admin.site.register(Firmware, FirmwareAdmin)


class PreprocessingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Preprocessing, PreprocessingAdmin)


class AlertContactGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(AlertContactGroup, AlertContactGroupAdmin)


class AlertContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(AlertContact, AlertContactAdmin)


class AlertAdmin(admin.ModelAdmin):
    pass


admin.site.register(Alert, AlertAdmin)


class AlertDependencyAdmin(admin.ModelAdmin):
    pass


admin.site.register(AlertDependency, AlertDependencyAdmin)
