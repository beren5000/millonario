# -*- coding: utf-8 -*-
from django.conf import  settings
from django.contrib import admin
from millonario.modulos.localizaciones.models import  *

class RegionesInline(admin.StackedInline):
    model = Regiones
    extra=5

class DepartamentosInline(admin.StackedInline):
    model = Departamentos
    extra=5
class CiudadesInline(admin.StackedInline):
    model = Ciudades
    extra=32

class PaisesAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    #list_filter = ['agrupaciontipo','peso']
    #readonly_fields=['idmapperfil']        
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA
    inlines =[RegionesInline]

class RegionesAdmin(admin.ModelAdmin):
    list_display = ['nombre','pais']
    list_filter = ['pais']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    inlines =[DepartamentosInline]
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class DepartamentosAdmin(admin.ModelAdmin):
    list_display = ['nombre','region']
    list_filter = ['region','region__pais']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    inlines =[CiudadesInline]
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class CiudadesAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_filter = ['departamento','departamento__region','departamento__region__pais']
    #readonly_fields=['idmapperfil']

    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class BarriosAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_filter = ['ciudad','ciudad__departamento','ciudad__departamento__region','ciudad__departamento__region__pais']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

admin.site.register(Paises,PaisesAdmin)
admin.site.register(Regiones,RegionesAdmin)
admin.site.register(Departamentos,DepartamentosAdmin)
admin.site.register(Ciudades,CiudadesAdmin)
admin.site.register(Barrios,BarriosAdmin)





