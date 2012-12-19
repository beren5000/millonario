# -*- coding: utf-8 -*-
from django.conf import  settings
from django.contrib import admin
from millonario.modulos.encuestas.models import  *

class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    #list_filter = ['agrupaciontipo','peso']
    #readonly_fields=['idmapperfil']        
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    #list_filter = ['agrupaciontipo','peso']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    #list_filter = ['agrupaciontipo','peso']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class GrupoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    #list_filter = ['agrupaciontipo','peso']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class SolucionesAdmin(admin.ModelAdmin):
    list_display = ['persona']
    search_fields =  ['persona']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Pregunta,PreguntaAdmin)
admin.site.register(Respuesta,RespuestaAdmin)
admin.site.register(Grupo,GrupoAdmin)
admin.site.register(Soluciones,SolucionesAdmin)






