# -*- coding: utf-8 -*-
from django.conf import  settings
from django.contrib import admin
from millonario.modulos.negocios.models import  *



class EmpresasAdmin(admin.ModelAdmin):
    list_display = ['nit','nombre','creado','modificado']

    search_fields =  ['nombre','nit']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class UensAdmin(admin.ModelAdmin):
    list_display = ['nombre','empresa','creado','modificado']
    list_filter = ['empresa']
    search_fields =  ['nombre','empresa__nit']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

admin.site.register(Empresas,EmpresasAdmin)
admin.site.register(Uens,UensAdmin)