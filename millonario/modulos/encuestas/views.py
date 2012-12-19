# -*- coding: utf-8 -*-
    # Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from millonario.settings import MEDIA_ROOT

from django.contrib.auth.decorators import login_required

from millonario.modulos.encuestas.models import *
from millonario.modulos.segmentacion.models import Sexo
from millonario.modulos.recursos.models import *

@login_required
def administrar(request):
    encuestas=Encuesta.objects.filter(activo=True)
    niveles=Grupo.objects.all()
    template = "administrador.html"
    data = {
        'encuestas': encuestas,
        'niveles':niveles,
        'estado':1
    }
    return render_to_response(template, data, context_instance=RequestContext(request))


def editar_nivel(request,encuesta_id,nivel_id):
    preguntas=Encuesta.objects.get(id=encuesta_id).render_preguntas_nivel(nivel_id)
    data={
            'estado':1,
            'preguntas':preguntas
        }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    #return HttpResponse(simplejson.dumps({'estado':0}),mimetype='application/json')
	
	
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
def desactivar_encuesta(request):
    if request.POST:
        encuesta=request.POST['encuesta']
        encuesta=Encuesta.objects.get(id=int(encuesta))
        encuesta.activo=False
        encuesta.save()
        data={'estado':1}
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
            'numero_preguntas':encuesta.numero_de_preguntas,
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
            'numero_preguntas':encuesta.numero_de_preguntas,
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

    encuestas = Encuesta.objects.filter(activo=True)
    results="<encuestas>"
    for encuesta in encuestas:
        results+="<encuesta id='"+str(encuesta.id)+"'>"+str(encuesta.nombre)+"</encuesta>"

    results += "</encuestas>"
    return HttpResponse(results, mimetype='text/xml')

@login_required
def concursar(request):
    encuestas=Encuesta.objects.filter(activo=True)
    cargos=Cargos.objects.all()
    data = {'encuestas': encuestas,'cargos':cargos}
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
        try:
            persona=Personas.objects.get(cedula=cedula)
            persona.full_name
            data={
                'estado':1,
                'persona_id':persona.id,
                'nombre':persona.full_name,
                'html':"",

            }
        except:
            html="""
            """
            data={
                'estado':0,
                'persona_id':-1,
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
#        try:
#
#            new_user, created = User.objects.get_or_create(str(cedula),"spam@spam.com",cedula)
#        except:
#            pass

        new_user = User()
        new_user.username=str(cedula)
        new_user.email="spam@spam.com"
        new_user.set_password(cedula)
        new_user.save()

        persona=Personas()
        persona.user=new_user
        persona.nombres=nombre
        persona.apellidos=apellido
        persona.sexo=sexo
        persona.cedula=str(cedula)
        persona.save()

        data={
            'estado':1,
            'persona_id':persona.id,
            'nombre':persona.nombres,
            'html':"",
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')

    data = {'estado': 0}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def xmlcedula(request):
    if request.method == "POST":
        aleatorio=request.POST['aleatorio']
        cedula=request.POST['cedula']
        persona=Personas.objects.get(cedula=cedula)

        xml="<?xml version='1.0' encoding='UTF-8'?><xml><data_cedula>"
        xml+="<idded>"+str(persona.id)+"</idded>"
        xml+="<named>"+persona.full_name +"</named>"
        xml+="</data_cedula></xml>"
        myfile = open(MEDIA_ROOT+'/xml/xmlcedula'+aleatorio+'.xml','w')
        myfile.write(xml.encode('ascii', 'ignore'))
        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')

@csrf_exempt
def xmljuego(request):
    if request.method == "POST":
        #persona_id=request.POST['persona_id']
        aleatorio=request.POST['aleatorio']
        encuestas=request.POST.getlist('encuestas[]')

        encuestas=map(lambda x: int(x[5:]), encuestas)

        #persona=Personas.objects.get(id=persona_id)
        encuestas=Encuesta.objects.filter(id__in=encuestas)

        xml="<?xml version='1.0' encoding='UTF-8'?><xml>"
        grupos=Grupo.objects.all()
        for g in grupos:
            xml+="<nivel"+str(g.id)+">"
            for e in encuestas:
                preguntas=Pregunta.objects.filter(encuesta=e,grupo=g)
                for p in preguntas:
                    xml+="<preguntas correcta='"+str(p.respuesta_correcta.id)+"'>"
                    xml+="<pregunta id='"+str(p.id)+"'>"+str(p.nombre)+"</pregunta>"
                    for r in p.respuestas:
                        xml+="<item id='"+str(r.id)+"'>"+str(r.nombre)+"</item>"
                    xml+="</preguntas>"
            xml+="</nivel"+str(g.id)+">"
        xml+="</xml>"
        myfile = open(MEDIA_ROOT+'/xml/xmlencuesta'+aleatorio+'.xml','w')
        myfile.write(xml.encode('ascii', 'ignore'))
        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')

@csrf_exempt
def enviar_datos(request):
    if request.method == "POST":

        persona_id=int(request.POST.getlist('datos')[0].split(',')[1])
        print persona_id,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        preguntas=request.POST.getlist('datos')[1].split(',')
        print preguntas,"YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

        persona=Personas.objects.get(id=persona_id)
        print persona

        for index in range(len(preguntas)):
            if index%2!=0:
                if preguntas[index]!="nada":
                    solucion=Soluciones()
                    solucion.persona=persona
                    res=Respuesta.objects.get(id=int(preguntas[index]))
                    solucion.respuesta=res
                    solucion.save()
                    print "salve"

        xml="<?xml version='1.0' encoding='UTF-8'?><xml><estado>1</estado></xml>"
        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')
