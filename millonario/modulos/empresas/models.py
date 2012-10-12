# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import get_model

# Create your models here.

class Maestra(models.Model):
    nombre=models.CharField(max_length=100,unique=True,blank=False,null=False)
    descripcion = models.TextField(blank=True,null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    jefe=models.ForeignKey('recursos.Personas',blank=True,null=True,limit_choices_to = {'es_jefe': True,'activo':True}) # los cargos pueden tener un arbol

    class Meta:
        ordering = ["nombre",'modificado']
        abstract = True
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Areas(Maestra):
    sub_area= models.ForeignKey('self',blank=True,null=True) # los cargos pueden tener un arbol
    uen= models.ForeignKey('negocios.Uens',blank=True,null=True) # los cargos pueden tener un arbol
    

    class Meta(Maestra.Meta):
        verbose_name_plural = "Area"
        verbose_name ="Area"
    def __unicode__(self):
        return u'Uen:%s Area:%s' % (self.uen,self.nombre)
class Departamentos(Maestra):
    sub_departamento= models.ForeignKey('self',blank=True,null=True) # los cargos pueden tener un arbol
    area = models.ForeignKey(Areas,blank=False,null=False) # los cargos pueden tener un arbol

    @property
    def uen(self):
        return self.area.uen

    class Meta(Maestra.Meta):
        verbose_name_plural = "Departamentos"
        verbose_name ="Departamento"


class Procesos(Maestra):
    sub_proceso= models.ForeignKey('self',blank=True,null=True) # los cargos pueden tener un arbol
    departamento = models.ForeignKey(Departamentos,blank=False,null=False) # los cargos pueden tener un arbol

    class Meta(Maestra.Meta):
        verbose_name_plural = "Procesos"
        verbose_name ="Proceso"
#    def save(self, *args, **kwargs):
#        personas= get_model('recursos', 'Personas')
#        super(rocesos, self).save(*args, **kwargs)
#        return personas.objects.filter(cargo__id=_self.id).update(jefe=self.jefe)
    @property
    def uen(self):
        return self.departamento.area.uen

# falta definir mejor los campos
class Cargos(Maestra):
    proceso = models.ForeignKey(Procesos,blank=True,null=True)
    sub_cargo= models.ForeignKey('self',blank=True,null=True) # los cargos pueden tener un arbol
    departamento = models.ForeignKey(Departamentos,blank=False,null=False) # los cargos pueden tener un arbol

    @property
    def uen(self):
        return self.departamento.area.uen
    def save(self, *args, **kwargs):
        personas= get_model('recursos', 'Personas')
        super(Cargos, self).save(*args, **kwargs)
        return personas.objects.filter(cargo__id=self.id).update(jefe=self.jefe)
    class Meta(Maestra.Meta):
        verbose_name_plural = "cargos"
        verbose_name ="cargo"

