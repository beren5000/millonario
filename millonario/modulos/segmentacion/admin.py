# -*- coding: utf-8 -*-
from django.contrib import admin
from millonario.modulos.segmentacion.models import *

class CiudadInline(admin.TabularInline):
    model = Ciudad

class AreaMetropolitanaAdmin(admin.ModelAdmin):
    inlines = [
        CiudadInline,
    ]

class CiudadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento']
    list_filter = ('departamento','departamento__region')
    search_fields = ["departamento__nombre",'nombre']
    related_search_fields = {'departamento': ('nombre',)}

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre',"region"]
    list_filter = ('region',)
    search_fields = ['nombre']


admin.site.register(Ciudad,CiudadAdmin)
admin.site.register(OperadorMovil)
admin.site.register(NumeroMovil)
admin.site.register(Departamento,DepartamentoAdmin)
admin.site.register(Escolaridad)
admin.site.register(IdeologiaPolitica)
admin.site.register(Religion)
admin.site.register(Edad)
admin.site.register(Sexo)
admin.site.register(Ocupacion)
admin.site.register(Region)
admin.site.register(AreaMetropolitana, AreaMetropolitanaAdmin)