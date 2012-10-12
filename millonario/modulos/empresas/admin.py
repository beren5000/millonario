
# -*- coding: utf-8 -*-
from django.conf import  settings
from django.contrib import admin
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from  millonario.modulos.empresas.models import  *

csrf_protect_m = method_decorator(csrf_protect)



#===============================================================================
# 
# #===============================================================================
# # class PSuperClienteForm(forms.ModelForm):
# #    class Meta:
# #        model = Cliente
# #    def clean(self):
# #        cleaned_data = self.cleaned_data        
# #        contrasena2 = cleaned_data.get("contrasena2")
# #        contrasena1= cleaned_data.get("contrasena1")
# #        if (contrasena2 !=contrasena1):
# #            self._errors["contrasena2"] = ErrorList([(u"LAS CONTRASEÑAS DEBEN SER IGUALES")])
# #            self._errors["contrasena1"] = ErrorList([(u"LAS CONTRASEÑAS DEBEN SER IGUALES")])            
# #            raise forms.ValidationError(u"ERROR DE CONTRASEÑAS")
# #        
# #        return cleaned_data
# #===============================================================================
#    
# class CampanaForm(forms.ModelForm):
#    contrasena2 = forms.CharField(widget=forms.PasswordInput())
#    contrasena1 = forms.CharField(widget=forms.PasswordInput())
#    
# 
#    def __init__(self, *args, **kwargs):
#        super(CampanaForm, self).__init__(*args, **kwargs)
#        instance = getattr(self, 'instance', None)
#        if instance and instance.id:
#            self.fields['nombre_usuario'].required = False
#            self.fields['nombre_usuario'].widget.attrs['readonly'] = True
#            #self.fields['email_usuario'].widget.attrs['readonly'] = True
#    class Meta:
#        model = Campana
#        #exclude = ['vendedor','user']
#    
#    def clean(self):
#        cleaned_data = self.cleaned_data        
#        contrasena2 = cleaned_data.get("contrasena2")
#        contrasena1= cleaned_data.get("contrasena1")
#        nombre_usuario= cleaned_data.get("nombre_usuario")
#        #email_usuario= cleaned_data.get("email_usuario")
#        
#        
#        #=======================================================================
#        # patron=re.compile(";|,|:")
#        # if len(patron.findall(nombre_usuario)) !=0:
#        #    self._errors["nombre_usuario"] = ErrorList([("CARATER INVALIDO")])
#        #    raise forms.ValidationError("CARATER INVALIDO EN NOMBRE_USUARIO")
#        #=======================================================================
#        
#        if (contrasena2 !=contrasena1):
#            self._errors["contrasena2"] = ErrorList([(u"LAS CONTRASEÑAS DEBEN SER IGUALES")])
#            self._errors["contrasena1"] = ErrorList([(u"LAS CONTRASEÑAS DEBEN SER IGUALES")])            
#            raise forms.ValidationError(u"ERROR DE CONTRASEÑAS")
#            
#        #=======================================================================
#        # if nombre_usuario!=None: 
#        #    if  User.objects.filter(Q(username__iexact=nombre_usuario)|Q(email__iexact=nombre_usuario)).count()!=0:
#        #        self._errors["nombre_usuario"] = ErrorList([("YA EXISTE UN USUARIO EN EL SISTEMA CON ESTA INFORMACICON")])
#        #        raise forms.ValidationError("USUARIO INVALIDO")
#        #=======================================================================
#    
#            #===================================================================
#            # if Perfil.objects.filter(Q(user__username__iexact=nombre_usuario)|Q(user__email__iexact=nombre_usuario)).count()!=0:
#            #    self._errors["nombre_usuario"] = ErrorList([("YA EXISTE UN USUARIO EN EL SISTEMA CON ESTA INFORMACICON")])
#            #    raise forms.ValidationError("USUARIO INVALIDO")
#            #===================================================================
# 
#         
#        return cleaned_data 
#    
# def desactivar_clientes(modeladmin, request, queryset):
#    sigma=queryset.update(activo=False)
#    messages.add_message(request, messages.warning, "Campañas Desactivados.%s"%(str(sigma)))
#    
# desactivar_clientes.short_description = u"Desactivar campañas"
# 
# def activar_clientes(modeladmin, request, queryset):
#    sigma=queryset.update(activo=True)
#    
#    messages.add_message(request, messages.success, "Campañas activados.%s"%(str(sigma)))
# activar_clientes.short_description = u"Activar campañas"
# 
# 
# class CampanaAdmin(AdminImageMixin,admin.ModelAdmin):
#    list_per_page=50
#    list_display = ('ultimo_acceso','nombre','fecha_de_finalizacion','mostrar_imagen','activo','impactos_a_fecha','clicks_restantes','clicks_comprados','clicks_consumidos_porcentual','ver_jugadas')
#    search_fields = ('nombre','numero_de_impatos_comprados__numero')
#    list_filter = ('activo','sexo','fecha_de_inicio','fecha_de_finalizacion','numero_de_impatos_comprados')
#    list_display_links = ('fecha_de_finalizacion','nombre', 'mostrar_imagen')
#    raw_id_fields = ('cliente', 'campana_anterior')    
#    filter_horizontal=['ideologiapolitica','religion','ciudad','departamento','escolaridad','operador_movil','edad']    
#    ordering = ('id',)
#    actions = [desactivar_clientes,activar_clientes]
#    #prepopulated_fields = {'nombre_slug': ('nombre',)}
#    #form=ClienteForm
#    class Media:
#        js = ('tiny_mce/tiny_mce.js','tiny_mce/textareas.js')
# 
#    
#    #===========================================================================
#    # #===========================================================================
#    # def get_actions(self, request):        
#    #    actions = super(ClienteAdmin, self).get_actions(request)
#    #    
#    #    if not(request.user.is_superuser) :            
#    #        del actions['desactivar_clientes']
#    #        del actions['activar_clientes']
#    #    return actions
#    # #===========================================================================
#    # 
#    # 
#    # def get_form(self, request, obj=None, **kwargs): 
#    #    if request.user.is_superuser: 
#    #        self.exclude = () 
#    #    else: 
#    #        self.exclude = ('vendedor','user','agencia','clicks','promedio_clicks_diarios','activo')
#    #        
#    #    return super(ClienteAdmin, self).get_form(request, obj=None, **kwargs) 
#    #    
#    #===========================================================================
#    #def get_form(self, request, obj=None, **kwargs):
#    #   return self.form
#        #=======================================================================
#        # if not request.user.is_superuser:
#        #    return SuperClienteForm
#        # else:
#        #    return ClienteForm       
#        #=======================================================================
#     
#    #===========================================================================
#          
# #===============================================================================
# #    def queryset(self, request):        
# #        qs = super(ClienteAdmin, self).queryset(request)
# #        if request.user.is_superuser:
# #            return qs        
# #        vendedor=get_object_or_404(Vendedor,user=request.user)
# #        #self.message_user(request, "Para soporte escriba a aguiar@aguiar.com." )       
# #        return qs.filter(vendedor=vendedor)      
# # 
# #    def save_model(self, request, obj, form, change):
# #        #como en el model save calculo el valor de los productos tambien toca
# #        #hacerlo aqui        
# #        
# #        # la primera vez se crear la factura si no es admin 
# #        
# #        if not(request.user.is_superuser) and not(change): # sino es root y no ha cambiado crea un nuevo object
# #            vendedor=get_object_or_404(Vendedor,user=request.user)
# #            new_user=User.objects.create_user(obj.nombre_usuario, obj.nombre_usuario, obj.contrasena1)
# #            new_user.is_staff=True
# #            new_user.save()            
# #            obj.user=new_user                                         
# #            obj.vendedor=vendedor
# #            obj.agencia=vendedor.agencia # para permitir filtrar por agencia
# #            obj.save() # generamos id
# #        
# #        if not(request.user.is_superuser) and change:
# #            vendedor=get_object_or_404(Vendedor,user=request.user)
# #            # sie el vendedor va modificar lo que realizo no hay problema
# #            if obj.vendedor==vendedor:                
# #                obj.save()    
# #        form.save_m2m()         # cualquier many to many se guarda
# #        self.message_user(request, "%s Procesado cone exito." % obj.nombre_usuario)
# #===============================================================================
# 
#    
# class PaginaEstaticaAdmin(admin.ModelAdmin):
#    class Media:
#        js = ('tiny_mce/tiny_mce.js','tiny_mce/textareas.js')
# 
# 
# class ClienteAdmin(admin.ModelAdmin):
#    pass
# 
# class ResponsablePautaAdmin(admin.ModelAdmin):
#    pass
# 
# class FacturacionPautaAdmin(admin.ModelAdmin):
#    list_per_page=50
#    raw_id_fields=['cliente','pauta']
#    filter_horizontal=['responsables_facturacion']
#===============================================================================

#===============================================================================
# class PremioPromocionalAdmin(AdminImageMixin,admin.ModelAdmin):
#    list_per_page=50
#    list_display = ('id','campana', 'tipo_de_premio','mostrar_campana','mostrar_imagen','activo')    
#    list_filter = ('fecha_de_inicio','fecha_de_finalizacion')
#    list_display_links = ('id','campana', 'tipo_de_premio')
#    filter_horizontal=['ciudad','edad','departamento','region']
#    readonly_fields=['cantidad_premios_entregados']
#    list_editable=['activo']
#    raw_id_fields=['tipo_de_premio','campana']
#    class Media:
#        js = ('tiny_mce/tiny_mce.js','tiny_mce/textareas.js')
# 
#    
# 
# class PremiosPorPerfilAdmin(admin.ModelAdmin):
#    list_per_page=50
#    list_display = ('perfil', 'mostrar_premio')    
#    list_filter = ('premio_promocional',)
#    list_display_links = ('perfil', 'mostrar_premio')    
#    filter_horizontal=['premio_promocional']
#    raw_id_fields=['perfil']
#===============================================================================


class AreasAdmin(admin.ModelAdmin):
    list_display = ['nombre','creado','modificado','sub_area','jefe','uen']
    list_filter = ['sub_area' ,'uen']
    raw_id_fields = ['sub_area','jefe','uen']
    #readonly_fields=['idmapperfil']        
    search_fields =  ['nombre']
   
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class Departamentosdmin(admin.ModelAdmin):
    list_display = ['nombre','creado','modificado','area','jefe','uen']
    list_filter = ['sub_departamento','area','area__uen']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    raw_id_fields = ['jefe','area','sub_departamento']
    list_per_page=settings.ELEMENTOS_POR_PAGINA


class CargosAdmin(admin.ModelAdmin):
    list_display = ['nombre','creado','modificado','departamento','jefe','uen','proceso']
    list_filter = ['departamento','departamento__area' ,'departamento__area__uen' ]
    #readonly_fields=['idmapperfil']
    list_editable = ['jefe']
    search_fields =  ['nombre']
    raw_id_fields = ['departamento','sub_cargo','jefe']
    list_per_page=settings.ELEMENTOS_POR_PAGINA

class ProcesosAdmin(admin.ModelAdmin):
    list_display = ['nombre','creado','modificado','departamento','sub_proceso','jefe','uen']
    list_filter = ['departamento' ,'departamento__area__uen' ,'sub_proceso','departamento__area' ,'jefe']
    #readonly_fields=['idmapperfil']
    search_fields =  ['nombre']
    list_per_page=settings.ELEMENTOS_POR_PAGINA
    raw_id_fields = ['jefe','sub_proceso','departamento']



admin.site.register(Areas,AreasAdmin)
admin.site.register(Departamentos,Departamentosdmin)
admin.site.register(Cargos,CargosAdmin)

admin.site.register(Procesos,ProcesosAdmin )



#admin.site.register(FlatPage, PaginaEstaticaAdmin)

