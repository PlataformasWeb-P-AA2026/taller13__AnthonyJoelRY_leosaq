from django.contrib import admin

from .models import Edificio, Departamento

class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'ciudad', 'tipo')
    search_fields = ('nombre', 'ciudad')
    list_filter = ('tipo',)
admin.site.register(Edificio, EdificioAdmin)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo_propietario', 'costo_departamento', 'numero_cuartos', 'edificio')
    search_fields = ('nombre_completo_propietario', 'edificio__nombre')
    list_filter = ('edificio',)
admin.site.register(Departamento, DepartamentoAdmin)
