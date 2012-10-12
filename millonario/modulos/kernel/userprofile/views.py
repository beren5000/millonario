# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.db import models
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login as userlogin
from django.contrib.auth.views import login
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.db.models import F
from millonario.modulos.segmentacion.models import *

from xml.dom import minidom
import urllib2
import random
import cPickle as pickle
import base64
from PIL import Image
import urllib
import os
from datetime import date
from dateutil.relativedelta import *

from millonario.modulos.kernel.userprofile.models import EmailValidation, Avatar
from millonario.modulos.kernel.perfil.models import Referencia, Perfil, SistemaDePuntos
from millonario.modulos.kernel.userprofile.forms import *
#from millonario.modulos.utilidades.decoradores.decoradores import   ajax_requerido
from dateutil.relativedelta import *
from datetime import date



if not settings.AUTH_PROFILE_MODULE:
    raise SiteProfileNotAvailable

Profile = Perfil
        
if not Profile:
    raise SiteProfileNotAvailable

if hasattr(settings, "DEFAULT_AVATAR") and settings.DEFAULT_AVATAR:
    DEFAULT_AVATAR = settings.DEFAULT_AVATAR
else:
    DEFAULT_AVATAR = os.path.join(settings.MEDIA_ROOT, "generic.jpg")

if not os.path.isfile(DEFAULT_AVATAR):
    import shutil

    image = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        "generic.jpg")
    shutil.copy(image, DEFAULT_AVATAR)

GOOGLE_MAPS_API_KEY = hasattr(settings, "GOOGLE_MAPS_API_KEY") and\
                      settings.GOOGLE_MAPS_API_KEY or None
AVATAR_WEBSEARCH = hasattr(settings, "AVATAR_WEBSEARCH") and\
                   settings.AVATAR_WEBSEARCH or None

if AVATAR_WEBSEARCH:
    import gdata.service
    import gdata.photos.service

def get_profiles():
    return Profile.objects.order_by("-date")


def fetch_geodata(request, lat, lng):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        url = "http://ws.geonames.org/countrySubdivision?lat=%s&lng=%s" % (lat, lng)
        dom = minidom.parse(urllib.urlopen(url))
        country = dom.getElementsByTagName('countryCode')
        if len(country) >= 1:
            country = country[0].childNodes[0].data
        region = dom.getElementsByTagName('adminName1')
        if len(region) >= 1:
            region = region[0].childNodes[0].data

        return HttpResponse(simplejson.dumps({'success': True, 'country': country, 'region': region}))
    else:
        raise Http404()


@never_cache
def public(request, username):
    try:
        profile = User.objects.get(username=username).get_profile()
    except:
        raise Http404

    template = "templates_game/userprofile/profile/public.html"
    data = {'profile': profile, 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY, }
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@never_cache
def searchimages(request):
    """
    Web search for images Form
    """

    images = dict()
    if request.method == "POST" and request.POST.get('keyword'):
        keyword = request.POST.get('keyword')
        gd_client = gdata.photos.service.PhotosService()
        feed = gd_client.SearchCommunityPhotos("%s&thumbsize=72c" % keyword.split(" ")[0], limit='48')
        for entry in feed.entry:
            images[entry.media.thumbnail[0].url] = entry.content.src

    template = "templates_game/userprofile/avatar/search.html"
    data = {'section': 'avatar', 'images': images, }
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def overview(request):
    """
    Main profile page
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        request.session.flush()
        logout(request)
        return HttpResponseRedirect(reverse('login'))

    validated = False
    try:
        email = EmailValidation.objects.get(user=request.user).email
    except EmailValidation.DoesNotExist:
        email = request.user.email
        if email: validated = True

    template = "templates_game/userprofile/profile/overview.html"
    data = {'section': 'overview', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
            'email': email, 'validated': validated, 'profile': profile}
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@never_cache
def personal(request):
    """
    Personal data of the user profile
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        request.session.flush()
        logout(request)
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, reconfirmar=False)
        if form.is_valid():
            ### no salvar el form aunque es poderoso es
            ### es mejor salvar la instacia leyendo los datos del formulario
            nombre = form.cleaned_data.get('nombre')
            profile.nombre = nombre.title()
            apellidos = form.cleaned_data.get('apellidos')
            profile.apellidos = apellidos.title()
            #profile.fecha_de_nacimiento = form.cleaned_data.get('fecha_de_nacimiento')
            ######################
            profile.acerca_de_mi = form.cleaned_data.get('acerca_de_mi')
            profile.direcion = form.cleaned_data.get('direcion')
            profile.celular = form.cleaned_data.get('celular')
            profile.barrio = form.cleaned_data.get('barrio')
            profile.telefono = form.cleaned_data.get('telefono')
            #profile.cedula = form.cleaned_data.get('cedula')
            #if not (form.cleaned_data['departamento'] in [None,'']):
            profile.operador_movil = form.cleaned_data.get('operador_movil')
            profile.departamento = form.cleaned_data['departamento']
            profile.estado_civil = form.cleaned_data['estado_civil']
            #if not (form.cleaned_data['ciudad'] in ['',None]):
            profile.ciudad = form.cleaned_data['ciudad']
            profile.region = profile.departamento.region
            profile.sexo = form.cleaned_data['sexo']
            profile.ocupacion = form.cleaned_data['ocupacion']
            #profile.email_activo=True
            profile.save()

            return HttpResponseRedirect(reverse("profile_edit_personal_done"))
        else:
            print form.errors, form.non_field_errors
    else:
        form = ProfileForm(instance=profile, reconfirmar=False)
    template = "templates_game/userprofile/profile/personal.html"
    data = {'section': 'personal', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
            'form': form, 'profile': profile}
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@never_cache
def reconfirmar_perfil(request):
    """
    Personal data of the user profile
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        request.session.flush()
        logout(request)
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        form = ProfileForm(request.POST, reconfirmar=True, instance=profile)
        if form.is_valid():
            ### no salvar el form aunque es poderoso es
            ### es mejor salvar la instacia leyendo los datos del formulario
            nombre = form.cleaned_data.get('nombre')
            profile.nombre = nombre.title()
            apellidos = form.cleaned_data.get('apellidos')
            profile.apellidos = apellidos.title()
            #profile.fecha_de_nacimiento = form.cleaned_data.get('fecha_de_nacimiento')
            ######################
            profile.acerca_de_mi = form.cleaned_data.get('acerca_de_mi')
            profile.direcion = form.cleaned_data.get('direcion')
            profile.celular = form.cleaned_data.get('celular')
            profile.barrio = form.cleaned_data.get('barrio')
            profile.telefono = form.cleaned_data.get('telefono')
            profile.cedula = form.cleaned_data.get('cedula')
            profile.operador_movil = form.cleaned_data.get('operador_movil')
            #if not (form.cleaned_data['departamento'] in [None,'']):
            profile.departamento = form.cleaned_data['departamento']
            profile.estado_civil = form.cleaned_data['estado_civil']
            #if not (form.cleaned_data['ciudad'] in ['',None]):
            profile.ciudad = form.cleaned_data['ciudad']
            profile.sexo = form.cleaned_data['sexo']
            profile.ocupacion = form.cleaned_data['ocupacion']
            profile.region = profile.departamento.region
            #profile.email_activo=True

            profile.save()

            return HttpResponseRedirect(reverse("jugar"))
        else:
            print form.errors, form.non_field_errors
    else:
        form = ProfileForm(instance=profile, reconfirmar=True)
    template = "templates_game/userprofile/account/reconfirmar_perfil.html"
    data = {'section': 'personal', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
            'form': form, 'profile': profile
    }
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@never_cache
def location(request):
    """
    Location selection of the user profile
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile_edit_location_done"))
    else:
        form = LocationForm(instance=profile)

    template = "templates_game/userprofile/profile/location.html"
    data = {'section': 'location', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
            'form': form, }
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def delete(request):
    if request.method == "POST":
        # Remove the profile and all the information
        #Profile.objects.filter(user=request.user).delete()
        EmailValidation.objects.filter(user=request.user).delete()
        Avatar.objects.filter(user=request.user).delete()

        # Remove the e-mail of the account too
        request.user.email = ''
        request.user.first_name = ''
        request.user.last_name = ''
        request.user.save()

        return HttpResponseRedirect(reverse("profile_delete_done"))

    template = "templates_game/userprofile/profile/delete.html"
    data = {'section': 'delete', }
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@never_cache
def avatarchoose(request):
    """
    Avatar choose
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    if not request.method == "POST":
        form = AvatarForm()
    else:
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data.get('url') or form.cleaned_data.get('photo')
            avatar = Avatar(user=request.user, image=image, valid=False)
            avatar.image.save("%s.jpg" % request.user.username, image)

            image = Image.open(avatar.image.path)
            image.thumbnail((480, 480), Image.ANTIALIAS)
            image.convert("RGB").save(avatar.image.path, "JPEG")
            avatar.save()
            #base, filename = os.path.split(avatar_path)
            #generic, extension = os.path.splitext(filename)

            return HttpResponseRedirect('%srecortar/' % request.path_info)

    if DEFAULT_AVATAR:
        base, filename = os.path.split(DEFAULT_AVATAR)
        filename, extension = os.path.splitext(filename)
        generic96 = "%s/%s.96%s" % (base, filename, extension)
        generic96 = generic96.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    else:
        generic96 = ""

    template = "templates_game/userprofile/avatar/choose.html"
    data = {'generic96': generic96, 'form': form,
            'AVATAR_WEBSEARCH': AVATAR_WEBSEARCH, 'section': 'avatar', 'profile': profile}
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
@never_cache
def avatarcrop(request):
    """
    Avatar management
    """
    avatar = get_object_or_404(Avatar, user=request.user, valid=False)
    if not request.method == "POST":
        form = AvatarCropForm()
    else:
        form = AvatarCropForm(request.POST)
        if form.is_valid():
            top = int(form.cleaned_data.get('top'))
            left = int(form.cleaned_data.get('left'))
            right = int(form.cleaned_data.get('right'))
            bottom = int(form.cleaned_data.get('bottom'))

            image = Image.open(avatar.image.path)
            box = [left, top, right, bottom]
            image = image.crop(box)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')

            image.save(avatar.image.path)
            avatar.valid = True
            avatar.save()
            return HttpResponseRedirect(reverse("profile_avatar_crop_done"))

    template = "templates_game/userprofile/avatar/crop.html"
    data = {'section': 'avatar', 'avatar': avatar, 'form': form, }
    return render_to_response(template, data, context_instance=RequestContext(request))


#@cache_control(must_revalidate=True, max_age=3600)
#@cache_page(60 * 45)
@login_required
def avatardelete(request, avatar_id=False):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            Avatar.objects.get(user=request.user, valid=True).delete()
            return HttpResponse(simplejson.dumps({'success': True}))
        except:
            return HttpResponse(simplejson.dumps({'success': False}))
    else:
        raise Http404()

#@cache_control(must_revalidate=True, max_age=3600)
#@cache_page(60 * 45)
@never_cache
def email_validation_process(request, key):
    """
    Verify key and change email
    """
    if EmailValidation.objects.verify(key=key):
        successful = True


    else:
        successful = False

    template = "templates_game/userprofile/account/email_validation_done.html"
    data = {'successful': successful, }
    return render_to_response(template, data, context_instance=RequestContext(request))

#@cache_control(must_revalidate=True, max_age=3600)
#@cache_page(60 * 45)
@never_cache
@login_required
def email_validation(request):
    """
    E-mail Change form
    """
    if request.method == 'POST':
        form = EmailValidationForm(request.POST)
        if form.is_valid():
            EmailValidation.objects.add(user=request.user, email=form.cleaned_data.get('email'))
            return HttpResponseRedirect('%sprocesado/' % request.path_info)
    else:
        form = EmailValidationForm()

    template = "templates_game/userprofile/account/email_validation.html"
    data = {'form': form, }
    return render_to_response(template, data, context_instance=RequestContext(request))


#@cache_control(must_revalidate=True, max_age=3600)
#@cache_page(60 * 45)
#@csrf_exempt
################################################################################
def first_step_register(request):
    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    tipo_referencia = TipoReferencia.objects.filter(activo=True)
    form = FirstStepRegistrationForm()
    referencias = []
    referencias_list = []
    for tipo in tipo_referencia:
        referencias.append({'tipo_referencia': tipo,
                            'referencias': Referencia.objects.filter(activo=True, tipo=tipo).order_by('-id')})
    if request.method == 'POST':
        form = FirstStepRegistrationForm(request.POST)
        referencias_list = map(lambda x: int(x), request.POST.getlist('referencia'))
        if form.is_valid():
            nuevo_perfil = form.save()
            username = form.cleaned_data.get('email1').replace(" ", "").lower()
            password = form.cleaned_data.get('password')
            newuser = authenticate(username=nuevo_perfil.user.username, password=password)
            userlogin(request, newuser)
            return HttpResponseRedirect(reverse('second_step'))
    template = "templates_game/userprofile/account/registration_first_step.html"
    data = {'form': form, 'tipo_referencia': tipo_referencia, 'referencias': referencias,
            'referencias_list': referencias_list, 'salida': salida}
    return render_to_response(template, data, context_instance=RequestContext(request))

################################################################################
def inviter_first_step_register(request, inviter_key):
    if not "inviter_key" in request.session:
        request.session['inviter_key'] = str(inviter_key)
    else:
        if request.session['inviter_key'] != str(inviter_key):
            request.session['inviter_key'] = str(inviter_key)

    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    tipo_referencia = TipoReferencia.objects.filter(activo=True)
    form = FirstStepRegistrationForm()
    referencias = []
    referencias_list = []
    try:
        try:
            id = int(inviter_key[40:])
        except ValueError:
            id = 0
        perfil = Perfil.objects.get(id=id)
        #perfil = Perfil.objects.get(inviter_key=inviter_key)
        for tipo in tipo_referencia:
            referencias.append(
                    {'tipo_referencia': tipo, 'referencias': Referencia.objects.filter(activo=True, tipo=tipo)})
        if request.method == 'POST':
            form = FirstStepRegistrationForm(request.POST)
            referencias_list = map(lambda x: int(x), request.POST.getlist('referencia'))
            if form.is_valid():
                nuevo_perfil = form.save()
                username = form.cleaned_data.get('email1').replace(" ", "").lower()
                password = form.cleaned_data.get('password')
                now = datetime.datetime.now()
                new_contact_register = ContactsRegister.objects.create(invite_profile=nuevo_perfil, user_profile=perfil,
                    creado=now)
                newuser = authenticate(username=username, password=password)
                userlogin(request, newuser)
                if "inviter_key" in request.session: del request.session["inviter_key"]
                return HttpResponseRedirect(reverse('second_step'))
        print request.session['inviter_key']
        template = "templates_game/userprofile/account/registration_first_step.html"
        data = {'form': form, 'tipo_referencia': tipo_referencia, 'referencias': referencias,
                'referencias_list': referencias_list, 'salida': salida}
        return render_to_response(template, data, context_instance=RequestContext(request))
    except Perfil.DoesNotExist:
        raise Http404

################################################################################
@login_required
def second_step_register(request):
    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    perfil = Perfil.objects.get(user=request.user)

    departamento = ''
    ciudad = ''

    default_data = {'nombre': perfil.nombre, 'apellidos': perfil.apellidos}
    if perfil.departamento:
        default_data.update({'departamento':perfil.departamento.id})

    if perfil.ciudad:
        default_data.update({'ciudad':perfil.ciudad.id})

    form = SecondStepRegistrationForm(default_data)
    if request.method == 'POST':
        form = SecondStepRegistrationForm(request.POST)
        if form.is_valid():
            form.save(perfil)
            return HttpResponseRedirect(reverse('third_step'))
        else:
            if "departamento" in request.POST:
                departamento = request.POST['departamento']
            else:
                departamento = 91

            if "ciudad" in request.POST:
                ciudad = request.POST['ciudad']
    return render_to_response("templates_game/userprofile/account/registration_second_step.html",
            {'form': form, 'departamento': departamento, 'ciudad': ciudad, 'salida': salida},
        context_instance=RequestContext(request))

################################################################################
@login_required
def third_step_register(request):
    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    perfil = Perfil.objects.get(user=request.user)


    default_data = {}
    if perfil.sexo:
        default_data.update({'sexo':perfil.sexo.id})

    if perfil.estado_civil:
        default_data.update({'estado_civil':perfil.estado_civil.id})

    if perfil.fecha_de_nacimiento:
        default_data.update({'mes':perfil.fecha_de_nacimiento.month,'dia':perfil.fecha_de_nacimiento.day,'ano':perfil.fecha_de_nacimiento.year})



    form = ThirdStepRegistrationForm(default_data)

    if request.method == 'POST':
        form = ThirdStepRegistrationForm(request.POST)
        if form.is_valid():
            form.save(perfil)
            return HttpResponseRedirect(reverse('fourth_step'))
    return render_to_response("templates_game/userprofile/account/registration_third_step.html",
            {'form': form, 'salida': salida},
        context_instance=RequestContext(request))

################################################################################
@login_required
def fourth_step_register(request):
    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    perfil = Perfil.objects.get(user=request.user)
    default_data = {'telefono': perfil.telefono, 'celular': perfil.celular,'estrato':perfil.estrato,'cedula':perfil.cedula}

    if perfil.operador_movil:
        default_data.update({'operador_movil':perfil.operador_movil.id})
    if perfil.ocupacion:
        default_data.update({'ocupacion':perfil.ocupacion.id})
    form = FourthStepRegistrationForm(default_data)

    form.cargar_perfil(perfil)
    if request.method == 'POST':
        form = FourthStepRegistrationForm(request.POST)
        form.cargar_perfil(perfil)




        if form.is_valid():
            form.save(perfil)
            return HttpResponseRedirect(reverse('jugar'))




    return render_to_response("templates_game/userprofile/account/registration_fourth_step.html",
            {'form': form, 'salida': salida},
        context_instance=RequestContext(request))

################################################################################
def register(request):
    form = RegistrationForm()
    departamento = ''
    ciudad=''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email').replace(" ", "").lower()
            password = form.cleaned_data.get('password1')
            nombre = form.cleaned_data.get('nombre')
            celular = form.cleaned_data.get('celular')
            telefono = form.cleaned_data.get('telefono')
            apellidos = form.cleaned_data.get('apellidos')
            cedula = form.cleaned_data.get('cedula')
            sexo = Sexo.objects.get(id=form.cleaned_data.get('sexo'))
            ano = form.cleaned_data.get('ano')
            mes = form.cleaned_data.get('mes')
            dia = form.cleaned_data.get('dia')
            fecha_de_nacimiento = datetime.date(ano, mes, dia)
            ciudad = Ciudad.objects.select_related().get(id=form.cleaned_data.get('ciudad'))
            departamento = form.cleaned_data.get('departamento')
            region = ciudad.departamento.region
            try:
                newuser = User.objects.create_user(username=username, email=username, password=password)
                #try:
                newuser.is_active = settings.ACTIVAR_USUARIO
                newuser.save()
                nuevo_perfil = Perfil(user=newuser, celular=celular, telefono=telefono, nombre=nombre,
                    apellidos=apellidos, cedula=cedula, sexo=sexo, ciudad=ciudad, region=region,
                    departamento=departamento, fecha_de_nacimiento=fecha_de_nacimiento)
                nuevo_perfil.save()
                referencias = form.cleaned_data.get('referencia')
                if len(referencias) != 0:
                    map(lambda referencia: nuevo_perfil.referencia.add(referencia), referencias)
                EmailValidation.objects.add(user=newuser, email=newuser.email)
                return HttpResponseRedirect(reverse('signup_complete'))
            except :
                newuser.delete()
        else:

            if "departamento" in request.POST:
                departamento = request.POST['departamento']
            else:
                departamento = 91

            if "ciudad" in request.POST:
                ciudad = request.POST['ciudad']
    template = "modulos/userprofile/account/registration.html"
    data = {'form': form, 'departamento': departamento,'ciudad':ciudad}
    return render_to_response(template, data, context_instance=RequestContext(request))

################################################################################
def inviter_register(request, perfil_id):
    form = RegistrationForm()
    departamento = ''
    try:
        id = int(perfil_id[40:])
        perfil = Perfil.objects.get(id=id)
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                nombre = form.cleaned_data.get('nombre')
                apellidos = form.cleaned_data.get('apellidos')
                cedula = form.cleaned_data.get('cedula')
                sexo = Sexo.objects.get(id=form.cleaned_data.get('sexo'))
                ano = form.cleaned_data.get('ano')
                mes = form.cleaned_data.get('mes')
                dia = form.cleaned_data.get('dia')
                fecha_de_nacimiento = datetime.date(ano, mes, dia)
                ciudad = Ciudad.objects.select_related().get(id=form.cleaned_data.get('ciudad'))
                departamento = form.cleaned_data.get('departamento')
                region = ciudad.departamento.region
                newuser = User.objects.create_user(username=username, email=username, password=password)
                try:
                    newuser.is_active = settings.ACTIVAR_USUARIO
                    newuser.save()
                    nuevo_perfil = Perfil(user=newuser, celular=celular, telefono=telefono, nombre=nombre,
                        apellidos=apellidos, cedula=cedula, sexo=sexo, ciudad=ciudad, region=region,
                        departamento=departamento, fecha_de_nacimiento=fecha_de_nacimiento)
                    nuevo_perfil.save()
                    nuevo_perfil.age()
                    referencias = form.cleaned_data.get('referencia')
                    if len(referencias) != 0:
                        map(lambda referencia: nuevo_perfil.referencia.add(referencia), referencias)
                    EmailValidation.objects.add(user=newuser, email=newuser.email)
                    new_contact_register = ContactsRegister.objects.create(invite_profile=nuevo_perfil,
                        user_profile=perfil, )
                    return HttpResponseRedirect('/registro/completo/')
                except:
                    newuser.delete()
            else:
                if request.POST.has_key('departamento'):
                    departamento = request.POST['departamento']
                else:
                    departamento = 91
        template = "templates_game/userprofile/account/registration.html"
        data = {'form': form, 'departamento': departamento}
        return render_to_response(template, data, context_instance=RequestContext(request))
    except Perfil.DoesNotExist:
        return Raise404

################################################################################
@login_required
def subscribe(request):
    user = request.user
    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    perfil = Perfil.objects.get(user=user)
    mensaje = 'No Hice un carajo'
    if request.method == 'POST':
        if perfil.unsubscribe_counter <= 2 and perfil.email_activo == False:
            perfil.email_activo = True
            mensaje = 'Tu cuenta de correo fue dada de Alta de nuevo, Gracias por Jugar ClickMillonario'
            perfil.save()
        else:
            mensaje = 'Tu cuenta ya no puede darse de alta debido a que tu email esta activo, o sobrepasaste el numero de veces que puedes realizar la operacion'
        return HttpResponseRedirect('/juego/jugar/')
    return render_to_response("templates_game/userprofile/account/subscribe.html",
            {'perfil': perfil, 'salida': salida, 'mensaje': mensaje},
        context_instance=RequestContext(request))

################################################################################
@login_required
def unsubscribe(request):
    user = request.user
    salida = settings.FECHA_DE_SALIDA
    now = datetime.datetime.now()
    salida = relativedelta(salida, now)
    perfil = Perfil.objects.get(user=user)
    if request.method == 'POST':
        if perfil.unsubscribe_counter <= 2:
            perfil.email_activo = False
            perfil.unsubscribe_counter = F('unsubscribe_counter') + 1
            perfil.save()
        else:
            user.is_active = False
            user.save()
        return HttpResponseRedirect(reverse('logout'))
    return render_to_response("templates_game/userprofile/account/unsubscribe.html",
            {'perfil': perfil, 'salida': salida},
        context_instance=RequestContext(request))

################################################################################
@login_required
@never_cache
def email_validation_reset(request):
    """
    Resend the validation email for the authenticated user.
    """
    perfil = Perfil.objects.get(user=request.user)
    try:
        resend = EmailValidation.objects.get(user=request.user).resend()
        response = "listo"
    except EmailValidation.DoesNotExist:
        response = "fallo"
        perfil.email_activo = True
        # agregar logica
        perfil.save()
    return HttpResponseRedirect(reverse("email_validation_reset_response", args=[response]))


@login_required
@never_cache
def mis_jugadas(request, lang='es'):
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        request.session.flush()
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    fecha_fin = str(date.today()) + " 00:00:00"
    fecha_ini = str(date.today() + relativedelta(days=-7)) + " 00:00:00"
    sql = 'SELECT   game_jugadasporjuego.*   FROM game_jugadasporjuego,game_juego   WHERE (game_juego.fecha_inicial BETWEEN "%s" and "%s" AND game_jugadasporjuego.perfil_id = %d and game_juego.id=game_jugadasporjuego.juego_id) GROUP by game_juego.id'
    tmp_jugadas = JugadasPorJuego.objects.raw(sql % (fecha_ini, fecha_fin, profile.id))
    jugadas_list = JugadasPorJuego.objects.filter(id__in=map(lambda x: x.id, tmp_jugadas))
    paginator = Paginator(jugadas_list, 4)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        jugadas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        jugadas = paginator.page(paginator.num_pages)

    return render_to_response("templates_game/userprofile/profile/historial.html",
            {'section': 'mis-jugadas', 'jugadas': jugadas, 'profile': profile},
        context_instance=RequestContext(request))


@never_cache
@login_required
def mis_premios(request, lang='es'):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        request.session.flush()
        logout(request)
        return HttpResponseRedirect(reverse('login'))

    fecha_fin = date.today()
    fecha_ini = fecha_fin + relativedelta(months=-2)
    premios_promocionales = []
    try:
        premios_perfil = PremiosPorPerfil.objects.get(perfil__user=request.user)
        premios_promocionales = premios_perfil.premio_promocional.filter(fecha_de_inicio__range=(fecha_ini, fecha_fin))
    except PremiosPorPerfil.DoesNotExist:
        premios_promocionales = []
    return render_to_response("templates_game/userprofile/profile/mis_premios.html",
            {'section': 'mis-premios', 'premios': premios_promocionales, 'profile': profile},
        context_instance=RequestContext(request))


@never_cache
@login_required
def contactos_registrados(request):
    contactos_registrados = ContactsRegister.objects.get(user_profile__user=request.user)
    return render_to_response("templates_game/userprofile/profile/contactos_registrados.html",
            {'section': 'contactos', 'contactos_registrados': contactos_registrados},
        context_instance=RequestContext(request))


@csrf_exempt
@never_cache
def login_profile(request, template_name, redirect_field_name, authentication_form):
    return login(request, template_name, redirect_field_name, authentication_form)


@never_cache
def referencias(request, referencia_id):
    referencias = Referencia.objects.filter(tipo__id=referencia_id)

    data = {'referencias': referencias}
    return render_to_response("templates_game/userprofile/account/referencias.html",
        data,
        context_instance=RequestContext(request))


###################################################################################################################VISTAS PUNTOS 
@login_required
def mispuntos(request):
    if 'profile' in request.session:
        profile = request.session['profile']
    else:
        profile = Perfil.objects.filter(user__id=request.user.id).only('nombre')[0]
        request.session['profile'] = profile

    puntos = SistemaDePuntos.objects.filter(perfil=profile)
    total_boletas=0
    if len(puntos) > 0:
        puntos = puntos[0]
        mispuntos = puntos.puntos_padre
        puntoshijos = puntos.puntos_hijos
        puntosnietos = puntos.puntos_nietos
        adicionales = puntos.puntos_adicionales
        total = puntos.mis_puntos
        total_boletas=total/540
        mishijos = profile.get_all_hijos
        data = {
            'total_boletas':total_boletas,
            'mispuntos': mispuntos,
            'puntoshijos': puntoshijos,
            'puntosnietos': puntosnietos,
            'adicionales': adicionales,
            'total': total,
            'mishijos': mishijos
        }
    else:
        data = {
            'total_boletas':total_boletas,
            'mispuntos': 0,
            'puntoshijos': 0,
            'puntosnietos': 0,
            'adicionales': 0,
            'total': 0,
            'mishijos': []
        }
    return render_to_response("templates_game/userprofile/account/mispuntos.html",
        data,
        context_instance=RequestContext(request))


@login_required
@csrf_exempt

def infohijo(request, id_hijo):
    hijo_nombre=''
    correo_hijo=''
    nietos=0

    if 'profile' in request.session:
        profile = request.session['profile']

    else:
        profile = Perfil.objects.filter(user__id=request.user.id).only('nombre')[0]
        request.session['profile'] = profile
    mensaje = ""
    hijo = ContactsRegister.objects.filter(user_profile=profile, invite_profile__id=id_hijo)
    if len(hijo) > 0:
        hijo = hijo[0]
        hijo_nombre = hijo.invite_profile.nombre
        correo_hijo = hijo.invite_profile.user.email
        vastagos = hijo.invite_profile.get_all_hijos
        try:
            nietos = []
            for i in vastagos:
                nietos += [[i.nombre, i.clicks_perfil * 2]]
        except:
            nietos = []
    return HttpResponse(simplejson.dumps({'hijo_nombre': hijo_nombre,
                                          'correo_hijo': correo_hijo,
                                          'nietos': nietos
    }), mimetype='application/json')


@login_required
@csrf_exempt

def matarhijo(request, id_hijo):
    if 'profile' in request.session:
        profile = request.session['profile']

    else:
        profile = Perfil.objects.filter(user__id=request.user.id).only('nombre')[0]
        request.session['profile'] = profile
    mensaje = ""
    hijo = ContactsRegister.objects.filter(user_profile=profile, invite_profile__id=id_hijo)
    if len(hijo) > 0:
        hijo = hijo[0]
        nombre = hijo.invite_profile.nombre
        hijo.delete()
        mensaje = nombre + " ya no es tu hijo"
    return HttpResponse(simplejson.dumps({'mensaje': mensaje}), mimetype='application/json')



@csrf_exempt
def consultar_usuario_cedula(request):
    data=[]
    if request.method == "POST":
        cedula = int(request.POST['cedula'])
        perfiles=Perfil.objects.filter(cedula=cedula)
        for perfil in perfiles:
            data.append({'perfil':perfil.nombres_apellidos,'usuario':perfil.user.username})

    return render_to_response("templates_game/userprofile/account/restaurar_usuario_cedula.html",
            {'data':data}, context_instance=RequestContext(request))


##################################  FIN VISTAS PUNTOS ###############################################################

def analitics(start_date, end_date):
    try:
        from googleanalytics import Connection
        from googleanalytics.data import DataPoint, DataSet
        import datetime

        google_account_email = 'clickmillonario@clickmillonario.com' # agregue el email de la cuenta de google analytics o la cuenta con que se registro
        google_account_password = '4Musdx0224' # UTILICE SU CUENTA POR FAVOR
        # SI METES EL PASSWORD MAL TE VA TIRAR 403 ERROR

        connection = Connection(google_account_email, google_account_password)
        accounts = connection.get_accounts() # aqui estan todas mis cuentas
        #print accounts[2].profile_id # aqui saque uno de mis cuentas  para saber que hay enn esa lista  dir(accounts[2]) y asi conoces mas aparte del profile_id
        # accounts[2].profile_id esto me devolvio  23492578
        # para entender mejor https://github.com/clintecker/python-googleanalytics/blob/master/USAGE.md
        # a mi pagina con id 23492578 le voy a calcular unos analytics
        account = connection.get_account(accounts[0].profile_id)

        #data = account.get_data(start_date, end_date, metrics=['visits'],dimensions=['city']) # tire el querys
        filters = []
        data_source = account.get_data(start_date=start_date, end_date=end_date, dimensions=['source'],
            metrics=['visits', ], sort=['-visits', ], filters=filters)
        data_source = map(lambda source: {'nombre': source[0][0], 'valor': source[1][0]}, data_source.list)
        ######################################################################################################################################################
        data_city = account.get_data(start_date, end_date, metrics=['visits'], dimensions=['city'],
            sort=['-visits', ]) # tire el querys
        data_city = map(lambda source: {'nombre': source[0][0], 'valor': source[1][0]}, data_city.list)
        return data_city, data_source
    except:
        return [], []


from django.contrib.auth.decorators import user_passes_test

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

import time

@staff_required(login_url="../seguimientos/")
def mi_analytics(request):
    from django.db import connection

    cursor = connection.cursor()
    sql = "SELECT id, fecha,usuarios FROM PERFILES_ACTUALES WHERE PERFILES_ACTUALES.fecha >= DATE_SUB(NOW(), INTERVAL 1 MONTH)"
    start_date = datetime.date(2011, 10, 04)
    end_date = datetime.date.today()

    if request.method == 'GET':
        if 'creado_ini' in request.GET and 'creado_ini' in request.GET:
            creado_fin = request.GET['creado_fin']
            creado_ini = request.GET['creado_ini']

            creado_fin = time.strptime(creado_fin, "%Y-%m-%d")

            end_date = datetime.date(creado_fin.tm_year, creado_fin.tm_mon, creado_fin.tm_mday)
            creado_fin = time.strftime("%Y-%m-%d", creado_fin)

            creado_ini = time.strptime(creado_ini, "%Y-%m-%d")
            start_date = datetime.date(creado_ini.tm_year, creado_ini.tm_mon, creado_ini.tm_mday)
            creado_ini = time.strftime("%Y-%m-%d", creado_ini)
            sql = "SELECT id, fecha,usuarios FROM PERFILES_ACTUALES WHERE PERFILES_ACTUALES.fecha  between  '%s' and '%s' " % (
            creado_ini, creado_fin)

    cursor.execute(sql)
    convertir_fecha = lambda (x, y, z): (int(x), int(y), int(z))
    total = 0
    listas = map(lambda (id, fecha, numero): {'llave': id, 'fecha': convertir_fecha(tuple(fecha.strftime('%Y-%m-%d').split("-"))), 'numero': numero},cursor.fetchall())
    total = sum(map(lambda x: x["numero"], listas))
    start_date=datetime.date(2012, 4, 16)
    analytics_ciudades, analytics_fuentes = analitics(start_date, end_date)
    return render_to_response("admin/analitics.html",
            {'listas': listas, 'sql': sql, 'total': total, 'analytics_ciudades': analytics_ciudades,
             'analytics_fuentes': analytics_fuentes}, context_instance=RequestContext(request))


from django.core.mail import send_mail
@staff_required(login_url="../seguimientos/")
def forzar_cambio_clave(request,perfil_id):
    perfil=Perfil.objects.get(id=perfil_id)
    user=perfil.user
    user.set_password(perfil.cedula)
    user.save()

    send_mail(u'Clickmillonario Cambio de clave para '+perfil.nombres_apellidos  , "Hola Como estas "+perfil.nombres_apellidos+' le asigno su cedula como clave. su nombre de usuario es ' +user.username + "  un abrazo para nosotros eres muy importante a jugar y ganar ", 'soporte@clickmillonario.com',
    ['soporte@clickmillonario.com',user.username,'socialmkt@clickmillonario.com'], fail_silently=False)
    return HttpResponseRedirect('http://ventas.clickmillonario.com/seguimientos/perfil/perfil/?q=%s'%(user.username) )




@csrf_exempt
def ajax_form_ciudad(request,id_departamento):
    if request.is_ajax() :
        if str(id_departamento).isdigit():
            ciudades=Ciudad.objects.filter(departamento__id=id_departamento)
        else:
            ciudades=Ciudad.objects.filter(departamento__nombre__iexact=id_departamento)

        data = { 'ciudades': ciudades }
        template = "modulos/ajaxhelpers/ciudades.html"
        return render_to_response(template,data, context_instance=RequestContext(request))
    else:
        response = HttpResponse()
        return response