# -*- coding: utf-8 -*-
    # Create your views here.
from django.db import transaction
import codecs
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Context
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from millonario.settings import MEDIA_ROOT

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.encoding import smart_str, smart_unicode

from millonario.modulos.encuestas.models import *
from millonario.modulos.segmentacion.models import Sexo
from millonario.modulos.recursos.models import *

@login_required
@staff_member_required
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
@staff_member_required
def concursar(request):
    encuestas=Encuesta.objects.filter(activo=True)
    uens=Uens.objects.all()
    sexos=Sexo.objects.all()
    data = {'encuestas': encuestas,'uens':uens,'sexos':sexos}
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
############## juan cambio aqui
#@transaction.commit_manually
@csrf_exempt
def userreg(request):
    if request.method == "POST":
        cedula=request.POST['cedula']
        nombre=request.POST['nombre']
        apellido=request.POST['apellidos']
        sexo=request.POST['sexo']
        sexo=Sexo.objects.get(id=int(sexo))
         
        try:
            try:
                new_user, created = User.objects.get_or_create(username=str(cedula),email="spam@spam.com",password=str(cedula))
            except:
                new_user=User.objects.get(username=str(cedula))
                
            
            new_user.set_password(cedula)
            new_user.save()
            
            
            persona,created=Personas.objects.get_or_create(user=new_user)
            persona.user=new_user
            persona.nombres=nombre
            persona.apellidos=apellido
            persona.sexo=sexo # el sexo probar que funcione
            persona.cedula=str(cedula)
            persona.save()

            data={
                'estado':1,
                'persona_id':persona.id,
                'nombre':persona.nombres,
                'html':"",
                }
        except:
            data={
                'estado':0,
                'error':"cedula ya registrada",
                }
        #else:
        #transaction.commit()
            
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    data = {'estado': 0, 'error':"ni lo intentes"}
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def xmlcedula(request):
    if request.method == "POST":
        aleatorio=request.POST['aleatorio']
        cedula=request.POST['cedula']
        persona=Personas.objects.get(cedula=cedula)

        xml=persona.render_xmlcedula
        myfile = open(MEDIA_ROOT+'/xml/xmlcedula'+aleatorio+'.xml','w')
        myfile.write(xml.encode('cp1252'))
        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')
import os
import sys
import shutil

def convert_to_utf8(filename):
    # gather the encodings you think that the file may be
    # encoded inside a tuple
    encodings = ('windows-1253', 'iso-8859-7', 'macgreek')

    # try to open the file and exit if some IOError occurs
    try:
        f = open(filename, 'r').read()
    except Exception:
        sys.exit(1)

    # now start iterating in our encodings tuple and try to
    # decode the file
    for enc in encodings:
        try:
            # try to decode the file with the first encoding
            # from the tuple.
            # if it succeeds then it will reach break, so we
            # will be out of the loop (something we want on
            # success).
            # the data variable will hold our decoded text
            data = f.decode(enc)
            break
        except Exception:
            # if the first encoding fail, then with the continue
            # keyword will start again with the second encoding
            # from the tuple an so on.... until it succeeds.
            # if for some reason it reaches the last encoding of
            # our tuple without success, then exit the program.
            if enc == encodings[-1]:
                sys.exit(1)
            continue

    # now get the absolute path of our filename and append .bak
    # to the end of it (for our backup file)
    fpath = os.path.abspath(filename)
    newfilename = fpath + '.bak'
    # and make our backup file with shutil
    shutil.copy(filename, newfilename)

    # and at last convert it to utf-8
    f = open(filename, 'w')
    try:
        f.write(data.encode('utf-8'))
    except Exception, e:
        print e
    finally:
        f.close()
        
############## juan cambio aqui
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
                    xml+="<pregunta id='"+str(p.id)+"'>"+p.nombre+"</pregunta>"
                    for r in p.respuestas:
                        xml+="<item id='"+str(r.id)+"'>"+r.nombre+"</item>"
                    xml+="</preguntas>"
            xml+="</nivel"+str(g.id)+">"
        xml+="</xml>"        

        myfile =  codecs.open(MEDIA_ROOT+'/xml/xmlencuesta'+aleatorio+'.xml', 'wU', 'cp1252')
        #xml = xml.decode('cp1252') # not 'ISO-8859-1'
        myfile.write(xml )
        myfile.close()
        
        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')

@csrf_exempt
def enviar_datos(request):
    if request.method == "POST":
        print request.POST, "REQUESTREQUESTREQUESTREQUESTREQUESTREQUESTREQUESTREQUEST"
        persona_id=int(request.POST.getlist('datos')[0].split(',')[1])
        contexto=request.POST.getlist('datos')[0].split(',')[0]
        print persona_id,"PERSONAIDPERSONAIDPERSONAIDPERSONAIDPERSONAIDPERSONAIDPERSONAID"
        preguntas=request.POST.getlist('datos')[1:]
        print preguntas, "PREGUNTASPREGUNTASPREGUNTASPREGUNTASPREGUNTASPREGUNTASPREGUNTAS"
        p=[]
        for pregunta in preguntas:
            pregunta=pregunta.split(',')
            if pregunta[0]!="":
                for id_pregunta in pregunta:
                    p+=[id_pregunta]
        preguntas=p
        print preguntas,"YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

        persona=Personas.objects.get(id=persona_id)
        print persona
        gano=ContextoSoluciones.objects.get(nombre="Gana")
        perdio=ContextoSoluciones.objects.get(nombre="Pierde")
        continua=ContextoSoluciones.objects.get(nombre="Continua")
        for index in range(len(preguntas)):
            if index != len(preguntas)-1:
                if index%2!=0:
                    if preguntas[index]!="nada":
                        solucion=Soluciones()
                        solucion.persona=persona
                        res=Respuesta.objects.get(id=int(preguntas[index]))
                        solucion.respuesta=res
                        solucion.contexto=continua
                        solucion.save()
                        print "salve"

            else:
                if preguntas[index]!="nada":
                    solucion=Soluciones()
                    solucion.persona=persona
                    res=Respuesta.objects.get(id=int(preguntas[index]))
                    solucion.respuesta=res
                    if contexto=="perdio":
                        solucion.contexto=perdio
                    else:
                        solucion.contexto=gano
                    solucion.save()
                    print "salve"

        xml="<?xml version='1.0' encoding='UTF-8'?><xml><estado>1</estado></xml>"
        return HttpResponse(xml, mimetype='text/xml')
    xml="<estado>0</estado>"
    return HttpResponse(xml, mimetype='text/xml')


@login_required
@staff_member_required
def reportes(request):
    gano=ContextoSoluciones.objects.get(nombre="Gana")
    perdio=ContextoSoluciones.objects.get(nombre="Pierde")
    ganadores=Soluciones.objects.filter(contexto=gano)
    perdedores=Soluciones.objects.filter(contexto=perdio)

    hombres_ganadores=ganadores.filter(persona__sexo__nombre='Hombre')
    mujeres_ganadoras=ganadores.filter(persona__sexo__nombre='Mujer')

    hombres_perdedores=perdedores.filter(persona__sexo__nombre='Hombre')
    mujeres_perdedoras=perdedores.filter(persona__sexo__nombre='Mujer')

    print hombres_ganadores,mujeres_ganadoras,hombres_perdedores,mujeres_perdedoras

    template = "reportes.html"
    data = {
        'hombres_ganadores':hombres_ganadores.count() ,
        'mujeres_ganadoras':mujeres_ganadoras.count(),
        'ganadores':ganadores.count(),
        'hombres_perdedores':hombres_perdedores.count(),
        'mujeres_perdedoras':mujeres_perdedoras.count(),
        'perdedores':perdedores.count()
    }
    return render_to_response(template, data, context_instance=RequestContext(request))

@csrf_exempt
def consultarcedula(request):
    if request.POST:
        cedula=request.POST['cedula']
        persona=Personas.objects.get(cedula=cedula)
        html=persona.render_soluciones
        data = {
            'estado':1,
            'html':html,
        }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    data = {
        'estado':0,
        'html':"La Cedula No Existe",
        }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@csrf_exempt
def consultartodo(request):
    print request
    if request.POST:

        soluciones=Soluciones.objects.all().exclude(contexto__nombre="Continua")
        data={
            'estado':1,
            'soluciones':soluciones,
            }
        html= render_to_string('reportecedula.html', data)
        data = {
            'estado':1,
            'html':html,
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    data = {
        'estado':0,
        'html':"La Cedula No Existe",
        }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@staff_member_required
def reportecsv(request):
#    # Create the HttpResponse object with the appropriate CSV header.
#    response = HttpResponse(mimetype='text/csv')
#    response['Content-Disposition'] = 'attachment; filename="reportesoluciones.csv"'
#
#    # The data is hard-coded here, but you could load it from a database or
#    # some other source.
#
#    soluciones=Soluciones.objects.all()
#
#    t = loader.get_template('reportecsv.csv')
#    c = Context({
#        'soluciones': soluciones,
#        })
#    response.write(t.render(c))
#    return response
    soluciones=Soluciones.objects.all().exclude(contexto__nombre='Continua')
    lCsvFile = render_to_string('reportecsv.csv', {
        "soluciones" : soluciones,
        })

    lResponse = HttpResponse(mimetype="text/csv")
    lResponse['Content-Disposition'] = 'attachment; filename="reportesoluciones.csv"'
    lResponse.write(lCsvFile.encode("cp1252"))
    return lResponse

@csrf_exempt
def loadcargos(request):
    if request.POST:
        uen_id=request.POST['uen']
        uen=Uens.objects.get(id=uen_id)
        html=uen.render_cargos
        data = {
            'estado':1,
            'html':html,
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    data = {
        'estado':0,
        'html':"la uen no existe",
        }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')
