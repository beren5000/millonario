# -*- coding: utf-8 -*-

# Create your models here.
from django.db import models

# Create your models here.
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
class Empresas(Maestra):


    nit=models.CharField(max_length=100,unique=True,blank=False,null=False)
    class Meta(Maestra.Meta):
        unique_together = ("nombre", "nit")
class Uens(Maestra):
    
    empresa = models.ForeignKey(Empresas,blank=True,null=True)
    class Meta(Maestra.Meta):
        verbose_name_plural = "Unidades  Estrategicas de negocios"
        verbose_name ="Unidad de negocio"

    def __unicode__(self):
        
        return u'Empresa:%s   Uen: %s' % (self.empresa,self.nombre)