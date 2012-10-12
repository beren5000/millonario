# -*- coding: utf-8 -*-


from django.db import models

# Create your models here.
class Maestra(models.Model):
    nombre=models.CharField(max_length=100,unique=True,blank=False,null=False)
    descripcion = models.TextField(blank=True,null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    class Meta:
        ordering = ["nombre"]
        abstract = True
    def __unicode__(self):
        return u'%s' % (self.nombre)
class Paises(Maestra):
    class Meta(Maestra.Meta):
        verbose_name_plural = "Paises"
        verbose_name ="Pais"

class Regiones(Maestra):
    pais=models.ForeignKey(Paises,blank=False,null=False)
    class Meta(Maestra.Meta):
        ordering = ["nombre",'pais']
        unique_together = [("nombre",'pais')]
        verbose_name_plural = "Regiones"
        verbose_name ="Region"

class Departamentos(Maestra):
    region=models.ForeignKey(Regiones,blank=False,null=False)
    class Meta(Maestra.Meta):
        ordering = ["nombre",'region']
        verbose_name_plural = "Departamentos"
        verbose_name ="Departamento"


class Ciudades(Maestra):
    departamento=models.ForeignKey(Departamentos,blank=False,null=False)
    class Meta(Maestra.Meta):
        ordering = ["nombre",'departamento']
        verbose_name_plural = "Ciudades"
        verbose_name ="Ciudad"

class Barrios(Maestra):
    ciudad=models.ForeignKey(Ciudades,blank=False,null=False)
    class Meta(Maestra.Meta):
        ordering = ["nombre",'ciudad']
        verbose_name_plural = "Barrios"
        verbose_name ="Barrio"

