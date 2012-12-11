    # Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from millonario.modulos.encuestas.models import *
from millonario.modulos.segmentacion.models import Sexo

def administrar(request):
    encuestas=Encuesta.objects.all()
    niveles=Grupo.objects.all()
    template = "administrador.html"
    data = {
        'encuestas': encuestas,
        'niveles':niveles,
        'estado':1
    }
    return render_to_response(template, data, context_instance=RequestContext(request))

@csrf_exempt
def ver_preguntas(request):
    if request.POST:
        preguntas=Encuesta.objects.get(id=int(request.POST['encuesta_id'])).render_preguntas
        data={
            'estado':1,
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
            'estado':1,
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
            'estado':1,
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
            'estado':1,
            'id':encuesta.id,
            'preguntas':preguntas
        }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def agregar_nivel(request):
    if request.method == "POST":
        nivel=request.POST['nombre']
        encuesta=request.POST['encuesta']

        nivel=Grupo(nombre=nivel)
        nivel.save()

        if int(encuesta)!=-1:
            encuesta=Encuesta.objects.get(id=int(encuesta))
            preguntas=encuesta.render_preguntas
            data={
                'estado':1,
                'preguntas':preguntas
            }
        else:
            data={
                'estado':2
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')


@csrf_exempt
def update(request):
    if request.method == "POST":
        tipo=int(request.POST['tipo'])
        id=int(request.POST['id'])
        nombre=request.POST['nombre']
        encuesta=request.POST['encuesta']

        if tipo==1:
            temp=Encuesta.objects.get(id=id)
        elif tipo==2:
            temp=Grupo.objects.get(id=id)
        elif tipo==3:
            temp=Pregunta.objects.get(id=id)
        elif tipo==4:
            temp=Respuesta.objects.get(id=id)
        temp.nombre=nombre
        temp.save()

        if int(encuesta)!=-1:
            encuesta=Encuesta.objects.get(id=int(encuesta))
            preguntas=encuesta.render_preguntas
            data={
                'estado':1,
                'preguntas':preguntas,
                'tipo':tipo,
                'nombre':nombre,
                'id':id
            }
        else:
            data={
                'estado':2,
                'tipo':tipo,
                'nombre':nombre,
                'id':id
            }

        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def update_selects(request):
    if request.method == "POST":
        tipo=int(request.POST['tipo'])
        id=int(request.POST['id'])
        id_cambio=int(request.POST['id_cambio'])
        encuesta=request.POST['encuesta']

        temp=Pregunta.objects.get(id=id)

        if tipo==1:
            temp.grupo=Grupo.objects.get(id=id_cambio)
            temp.save()
        elif tipo==2:

            temp2=temp.respuestas.get(es_correcta=True)
            temp2.es_correcta=False
            temp2.save()
            temp2=temp.respuestas.get(id=id_cambio)
            temp2.es_correcta=True
            temp2.save()


        if int(encuesta)!=-1:
            encuesta=Encuesta.objects.get(id=int(encuesta))
            preguntas=encuesta.render_preguntas
            data={
                'estado':1,
                'preguntas':preguntas,
                'tipo':tipo,
                'id_cambio':id_cambio,
                'id':id
            }
        else:
            data={
                'estado':2,
                'preguntas':"<div></div>",
                'tipo':tipo,
                'id_cambio':id_cambio,
                'id':id
            }

        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')


@csrf_exempt
def xmlencuestas(request):

    encuestas = Encuesta.objects.all()
    results="<encuestas>"
    for encuesta in encuestas:
        results+="<encuesta id='"+str(encuesta.id)+"'>"+str(encuesta.nombre)+"</encuesta>"

    results += "</encuestas>"
    return HttpResponse(results, mimetype='text/xml')

def concursar(request):
    encuestas=Encuesta.objects.all()
    data = {'encuestas': encuestas}
    template = "concursar.html"
    return render_to_response(template, data, context_instance=RequestContext(request))

@csrf_exempt
def renderuserlog(request):
    html="""

        """
    data={
        'estado':1,
        'html':html,
    }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def userlog(request):
    if request.method == "POST":
        cedula=request.POST['cedula']
        usuario=User()
        try:
            perfil=Perfil.objects.get(cedula=cedula)
            data={
                'estado':1,
                'perfil_id':perfil.id,
                'nombre':perfil.nombre,
                'html':"",

            }
        except:
            html="""
            """
            data={
                'estado':0,
                'perfil_id':-1,
                'nombre':"No Existe el Usuario",
                'html':html,
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def userreg(request):
    if request.method == "POST":
        cedula=request.POST['cedula']
        nombre=request.POST['nombre']
        apellido=request.POST['apellidos']
        sexo=request.POST['sexo']

        sexo=Sexo.objects.get(id=int(sexo))
        new_user = User.objects.create_user(username=cedula,email=None, password=cedula)
        new_user.save()
        perfil=Perfil.objects.create(user=new_user, nombre=nombre, apellidos=apellido, sexo=sexo, cedula=int(cedula))
        perfil.save()

        data={
            'estado':1,
            'perfil_id':perfil.id,
            'nombre':perfil.nombre,
            'html':"",
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def xmljuego(request):
    if request.method == "POST":
        perfil_id=request.POST['perfil_id']
        encuestas=request.POST['encuestas']

        perfil=Perfil.objects.get(id=perfil_id)
        encuestas=Encuesta.objects.filter(id__in=encuestas)
        xml="<xml>"
        xml+="<usuario id="+perfil_id+">"+perfil.nombre +"</usuario>"

        grupos=Grupo.objects.all()
        for g in grupos:
            xml+="<nivel nivel="+g.id+">"
            for e in encuestas:
                preguntas=Pregunta.objects.filter(encuesta=e,grupo=g)
                for p in preguntas:
                    xml+="<preguntas correcta="+p.respuesta_correcta.id+">"
                    xml+="<pregunta id="+p.id+">"+p.nombre+"</pregunta>"
                    for r in p.respuestas:
                        xml+="<item id="+r.id+">"+r.nombre+"</item>"
                    xml+="</preguntas>"
            xml+="</nivel>"
        xml+="</xml>"

        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')