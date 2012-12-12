# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from millonario.modulos.empresas.models import  Cargos,Procesos
from millonario.modulos.localizaciones.models import  Barrios,Ciudades
from millonario.modulos.negocios.models import Uens
from django.core.exceptions import ValidationError

# Create your models here.

SEXO= (('F', 'FEMENINO'), ('M','MASCULINO' ))


class Maestra(models.Model):
    nombre=models.CharField(max_length=100,unique=True,blank=False,null=False)
    descripcion = models.TextField(blank=True,null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    class Meta:
        ordering = ["nombre",'modificado']
        abstract = True
    def __unicode__(self):
        return u'%s' % (self.nombre)

class TipoDePersona(Maestra):
    pass



def tiene_espacios(value):
    if value.count(" ")!=0:
        raise ValidationError(u'%s Se encontraron espacios' % value)
    if value.count("\t")!=0:
        raise ValidationError(u'%s Se encontraron tabs' % value)

class Personas(models.Model):

    """
    Stores a single blog entry, related to :model:`blog.Blog` and
    :model:`Recursos.Personas`.


    """
    codigo = models.BigIntegerField(blank=True,null=True)
    user = models.ForeignKey(User, unique=True)
    cedula=models.CharField(max_length=100,validators=[tiene_espacios],db_index=True,unique=True,blank=False,null=False,help_text="documento de identificacion del usuario ")
    nombres=models.CharField(max_length=100,db_index=True,blank=False,null=False)
    apellidos=models.CharField(max_length=100,db_index=True,blank=False,null=False)
    direccion = models.CharField(max_length=250, blank=True)
    telefono = models.CharField(null=True,max_length=250, blank=True)
    descripcion = models.TextField(blank=True,null=True)
    efectividad=models.DateTimeField(blank=True,null=True)

    sexo= models.CharField(max_length=1, db_index=True,blank=False,null=False,choices=SEXO)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)


    ciudad=models.ForeignKey(Ciudades,blank=True,null=True)
    barrio=models.ForeignKey(Barrios,blank=True,null=True)

    uen=models.ForeignKey(Uens,blank=True,null=True)
    cargo=models.ForeignKey(Cargos,blank=True,null=True)
    proceso=models.ForeignKey(Procesos,blank=True,null=True)



    jefe=models.ForeignKey('self',editable=False,limit_choices_to = {'es_jefe': True,'activo':True},blank=True,null=True) # los cargos pueden tener un arbol
    tipo_de_persona=models.ForeignKey('recursos.TipoDePersona',blank=True,null=True ,limit_choices_to = {'activo':True}) # los cargos pueden tener un arbol
    es_jefe=models.BooleanField(db_index=False,default=False)
    activo=models.BooleanField(db_index=True,default=True)


    def save(self, *args, **kwargs):
        #self.nombre_slug= defaultfilters.slugify(self.nombre)
        self.cedula=self.cedula.replace("\t","").replace(" ","")
        super(Personas, self).save(*args, **kwargs)


    @property
    def nombre_completo(self):
        return u'%s %s Cc:%s ' % (self.nombres, self.apellidos, self.cedula)
    @property
    def full_name(self):
        return u'%s %s ' % (self.nombres, self.apellidos)
    def __unicode__(self):
        return u'%s' % (self.nombre_completo)
    class Meta:
        ordering = ["cedula",'nombres','sexo']
        verbose_name_plural = "Personas"
        verbose_name ="Personas"

class Gerentes(Personas):
    class Meta:
        ordering = ["cedula",'nombres','sexo']
        proxy=True
        verbose_name_plural = "Gerentes"
        verbose_name ="Gerente"

class Presidentes(Personas):
    class Meta:
        ordering = ["cedula",'nombres','sexo']
        proxy=True
        verbose_name_plural = "Presidente"
        verbose_name ="President"

class Directivos(Personas):
    class Meta:
        ordering = ["cedula",'nombres','sexo']
        proxy=True
        verbose_name_plural = "Directivos"
        verbose_name ="Directivo"

class Empleados(Personas):
    class Meta:
        ordering = ["cedula",'nombres','sexo']
        proxy=True
        verbose_name_plural = "Empleados"
        verbose_name ="Empleado"
