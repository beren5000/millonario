# -*- coding: utf-8 -*-
from django.contrib import admin
from millonario.modulos.kernel.perfil.models import SistemaDePuntos, Perfil, ProcesarEmailBounce, EmailBounce, Referencia, TipoReferencia, VisitasReferenciasFecha, TopPerfilesInvitados

from django import forms


class PerfilAdmin(admin.ModelAdmin):
    list_display = (
    'nombre', 'apellidos','telefono','celular','cedula','fecha_de_nacimiento','estrato','user',  'cambiar_clave' ,'mostrar_usuario','fecha_registro', 'sexo', 'ciudad', 'region', 'departamento',
     'edad', 'hora_registro')
    search_fields = ('nombre', 'cedula', 'apellidos', 'user__username')
    list_filter = ['perfil_completo','sexo', 'ciudad', 'region', 'departamento', 'estado_civil', 'operador_movil', 'creado']
    raw_id_fields = ['user']
    list_display_links = ['user','nombre','apellidos']
    list_editable = ['fecha_de_nacimiento','cedula','estrato']
    list_per_page = 50

    class Media:
        js = ['/media/grappelli/media/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/media/grappelli/media/tinymce_setup/tinymce_setup.js', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overriden by the user in subclasses. In such case it should
        return True if the given request has permission to change the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to change *any* object of the given type.
        """
        #if not(request.user.is_superuser):
        #   self.readonly_fields=('fecha_de_nacimiento','date','telefono','celular','cedula','inviter_key','nombre', 'apellidos', 'user', 'fecha_registro','fecha_de_nacimiento','sexo','ciudad','region','departamento','estado_civil','operador_movil','edad','operador_movil','estado_civil','activado_desde_facebook','referencia','user','sexo')
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())


    def save_model(self, request, obj, form, change):
        form.save(commit=False)
        #if not set(obj.user.username).issubset("0123456789"):
        #       return form
        #else:
        obj.save()
        #obj.age()
        form.save_m2m()


class ProcesarEmailBounceAdmin(admin.ModelAdmin):
    list_display = ('csv_file_path', 'creado', 'modificado')
    #search_fields = ('user__email','user__username')
    list_filter = ['creado', 'modificado']


class EmailBounceAdmin(admin.ModelAdmin):
    list_display = ('tipo_de_error', 'correo_eletronico', 'razon', 'total_devueltos', 'creado', 'modificado')
    list_filter = ['creado', 'modificado']
    #search_fields = ('user__email','user__username')


class TipoReferenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'modificado')
    #search_fields = ('user__email','user__username')
    list_filter = ['creado', 'modificado']


class ReferenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'mostrar_imagen', 'tipo', 'modificado')
    search_fields = ('nombre',)
    list_filter = ['creado', 'tipo', 'modificado']


class VisitasReferenciasFechaAdmin(admin.ModelAdmin):

    list_display = (
    'referencia', 'fecha_registro', 'tipo_referencia', 'cantidad', 'region', 'departamento', 'ciudad', 'sexo')
    search_fields = ('tipo_referencia', 'referencia')
    list_filter = ['region', 'departamento', 'ciudad', 'sexo', 'fecha_registro', 'referencia', 'tipo_referencia']


class TopPerfilesInvitadosAdmin(admin.ModelAdmin):
    list_display = ['invitados', 'invitados_efectivos', 'creado', 'nombre', 'apellidos', 'region', 'departamento',
                    'ciudad', 'sexo', 'correo']
    search_fields = ('nombre', 'apellidos')
    list_filter = ['region', 'departamento', 'ciudad', 'sexo']


class SistemaDePuntosAdmin(admin.ModelAdmin):
    #@juan&francisco83
    list_display = (
    'correo', 'cedula', 'nombre_completo', 'ciudad', 'departamento', 'clickero', 'puntos_adicionales', 'numero_hijos',
    'puntos_padre', 'puntos_hijos', 'puntos_nietos', 'mis_puntos')
    search_fields = ('perfil__nombre', 'perfil__cedula', 'perfil__apellidos', 'perfil__user__username')
    list_filter = ['perfil__sexo', 'perfil__ciudad', 'perfil__region', 'perfil__departamento', 'perfil__estado_civil',
                   'perfil__operador_movil', 'perfil__creado']
    raw_id_fields = ['perfil']
    list_editable = ['puntos_adicionales', 'clickero']
    list_per_page = 50


admin.site.register(TipoReferencia, TipoReferenciaAdmin)
admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(ProcesarEmailBounce, ProcesarEmailBounceAdmin)
admin.site.register(EmailBounce, EmailBounceAdmin)
admin.site.register(VisitasReferenciasFecha, VisitasReferenciasFechaAdmin)
admin.site.register(TopPerfilesInvitados, TopPerfilesInvitadosAdmin)
admin.site.register(SistemaDePuntos, SistemaDePuntosAdmin)


