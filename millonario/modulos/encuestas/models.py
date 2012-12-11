from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from millonario.modulos.kernel.perfil.models import Perfil

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

class Pregunta(Maestra):
    encuesta = models.ForeignKey(Encuesta)
    grupo = models.ForeignKey(Grupo)

    @property
    def respuestas(self):
        return Respuesta.objects.filter(pregunta__id=self.id).order_by('id')

    @property
    def respuesta_correcta(self):
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

