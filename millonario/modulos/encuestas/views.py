    # Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from millonario.modulos.encuestas.models import *

def administrar(request):
    encuestas=Encuesta.objects.all()
    template = "administrador.html"
    data = {'encuestas': encuestas }
    return render_to_response(template, data, context_instance=RequestContext(request))

@csrf_exempt
def ver_preguntas(request):
    if request.POST:
        preguntas=Encuesta.objects.get(id=int(request.POST['encuesta_id'])).render_preguntas
        data={
            'preguntas':preguntas
        }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    return HttpResponse(simplejson.dumps({'estado':0}),mimetype='application/json')

@csrf_exempt
def eliminar_pregunta(request):
    if request.POST:
        pregunta=Pregunta.objects.get(id=int(request.POST['pregunta_id']))
        encuesta=Encuesta.objects.get(id=pregunta.encuesta_id)
        respuestas=Respuesta.objects.filter(pregunta__id=pregunta.id)

        for r in respuestas:
            r.delete()

        pregunta.delete()

        preguntas=encuesta.render_preguntas

        data={
            'preguntas':preguntas
        }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    return HttpResponse(simplejson.dumps({'estado':0}),mimetype='application/json')


@csrf_exempt
def agregar_pregunta(request):
    if request.method == "POST":
        pregunta=request.POST['nombre']

        res1=request.POST['res1']
        res2=request.POST['res2']
        res3=request.POST['res3']
        res4=request.POST['res4']
        respuestas=[[res1,0],[res2,0],[res3,0],[res4,0]]

        correcta=int(request.POST['correcta'])
        respuestas[correcta][1]=1

        encuesta=Encuesta.objects.get(id=int(request.POST['encuesta_id']))

        grupo=Grupo.objects.get(id=int(request.POST['grupo']))
        p=Pregunta(grupo=grupo,nombre=pregunta,encuesta=encuesta)

        p.save()

        for respuesta in respuestas:
            r=Respuesta(es_correcta=respuesta[1],nombre=respuesta[0],pregunta=p)
            r.save()

        preguntas=Encuesta.objects.get(id=int(request.POST['encuesta_id'])).render_preguntas
        data={
            'preguntas':preguntas
        }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')


@csrf_exempt
def agregar_encuesta(request):
    if request.method == "POST":
        encuesta=request.POST['nombre']
        encuesta=Encuesta(nombre=encuesta)

        encuesta.save()

        preguntas=encuesta.render_preguntas
        data={
            'id':encuesta.id,
            'preguntas':preguntas
        }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')