# -*- coding: utf-8 -*-
from django.db import models
from millonario.modulos.segmentacion.managers import CiudadManager

class Publication(models.Model):


    image =  models.CharField(db_index=True,max_length=255, blank=False)
    image_initialdir =  models.CharField(db_index=True,max_length=255, blank=False)
    image_extensions =  models.CharField(db_index=True,max_length=255, blank=False)
    image_format =  models.CharField(db_index=True,max_length=255, blank=False)
    pdf =  models.CharField(db_index=True,max_length=255, blank=False)


class Region(models.Model):
    
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)
    def __str__(self):
        return u'%s' % (self.nombre)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Regione"
        unique_together = ["nombre"]
        
class Departamento(models.Model):
    
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    region = models.ForeignKey(Region,related_name="Regiones")
    def __unicode__(self):
        return u'%s' % (self.nombre)

    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Departamento"
        unique_together = ["nombre"]


class AreaMetropolitana(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)
        
        
        
class Ciudad(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False)
    departamento = models.ForeignKey(Departamento,related_name="Departamentos")
    area_metropolitana = models.ForeignKey(AreaMetropolitana,related_name="Area Metropolitana", blank=True,null=True)
    cabecera = models.NullBooleanField(blank=True,null=True)
    objects=CiudadManager()
    def __unicode__(self):
        return u'%s' % (self.nombre)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Ciudade"

class Escolaridad(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    def __unicode__(self):
        return u'%s' % (self.nombre)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Escolaridade"

class Religion(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Religione"

    def __unicode__(self):
        return u'%s' % (self.nombre)

class IdeologiaPolitica(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Politica"
    def __unicode__(self):
        return u'%s' % (self.nombre)


class NumeroMovil(models.Model):
    numero = models.PositiveIntegerField(db_index=True,default=3,unique=True)
    class Meta:
        ordering = [ 'numero']
        verbose_name = "Numeros por operador"
    def __unicode__(self):
        return u'%s' % (self.numero)

class OperadorMovil(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    numero= models.ManyToManyField(NumeroMovil)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Operadores movile"
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Edad(models.Model):
    numero = models.PositiveSmallIntegerField(default=18)

    class Meta:
        ordering = [ 'numero']
        verbose_name = "Edade"
    def __unicode__(self):
        return u'%s' % (self.numero)

class Sexo(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Sexo"
    def __unicode__(self):
        return u'%s' % (self.nombre)


class EstadoCivil(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Estado civil"
    def __unicode__(self):
        return u'%s' % (self.nombre)
    
class Ocupacion(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Ocupacione"
    def __unicode__(self):
        return u'%s' % (self.nombre)


class Profesion(models.Model):
    nombre = models.CharField(db_index=True,max_length=255, blank=False,unique=True)
    class Meta:
        ordering = [ 'nombre']
        verbose_name = "Profesion"
    def __unicode__(self):
        return u'%s' % (self.nombre)