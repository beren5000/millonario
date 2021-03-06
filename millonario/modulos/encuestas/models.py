# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from millonario.modulos.recursos.models import Personas

# Create your models here.

class Maestra(models.Model):
    nombre=models.CharField(max_length=100,null=False)
    descripcion = models.TextField(blank=True,null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    class Meta:
        ordering = ["nombre",'modificado']
        abstract = True
    def __unicode__(self):
        return u'%s' % (self.nombre)


class Grupo(Maestra):
    pass

class Encuesta(Maestra):

    @property
    def numero_de_preguntas(self):
        return Pregunta.objects.filter(encuesta__id=self.id).count()

    @property
    def render_preguntas(self):
        preguntas=Pregunta.objects.filter(encuesta__id=self.id).order_by('grupo','id')
        grupos=Grupo.objects.all().order_by('id')
        data={
            'preguntas':preguntas,
            'grupos':grupos,
            'encuesta':self

        }
        return render_to_string('formulario.html', data)

    def render_preguntas_nivel(self,nivel):
        preguntas=Pregunta.objects.filter(encuesta__id=self.id,grupo__id=nivel).order_by('grupo','id')
        grupos=Grupo.objects.all().order_by('id')
        data={
            'preguntas':preguntas,
            'grupos':grupos,
            'encuesta':self

        }
        return render_to_string('formulario.html', data)

class Pregunta(Maestra):
    encuesta = models.ForeignKey(Encuesta)
    grupo = models.ForeignKey(Grupo)

    @property
    def respuestas(self):
        return Respuesta.objects.filter(pregunta__id=self.id).order_by('?')

    @property
    def respuesta_correcta(self):
        #print self.id
        #print Respuesta.objects.filter(pregunta__id=self.id, es_correcta=True)
        return Respuesta.objects.filter(pregunta__id=self.id, es_correcta=True)[0]





class Respuesta(models.Model):
    nombre=models.CharField(max_length=100,blank=False,null=False)
    descripcion = models.TextField(blank=True,null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    es_correcta=models.BooleanField(default=False)
    pregunta = models.ForeignKey(Pregunta)

    class Meta:
        ordering = ["nombre",'modificado']
    def __unicode__(self):
        return u'%s' % (self.nombre)


class ContextoSoluciones(Maestra):
    pass

class Soluciones(models.Model):
    persona = models.ForeignKey(Personas)
    respuesta = models.ForeignKey(Respuesta)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    contexto=models.ForeignKey(ContextoSoluciones)


