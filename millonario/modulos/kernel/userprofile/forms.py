# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django.utils.encoding import  force_unicode
from django.utils.html import  conditional_escape
from django.utils.safestring import mark_safe
from itertools import chain
from django import forms
from django.forms.widgets import SelectMultiple, CheckboxInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

import mimetypes, urllib, datetime
from dateutil.relativedelta import relativedelta
from millonario.modulos.kernel.perfil.models import  Perfil, Referencia, TipoReferencia
from millonario.modulos.kernel.userprofile.models import EmailValidation
from millonario.modulos.segmentacion.models import *
import calendar

if not settings.AUTH_PROFILE_MODULE:
    raise SiteProfileNotAvailable

Profile = Perfil
email_dict = {'class': 'font15 futura radius reg-input'}

attrs_dict = {'class': 'font15 futura radius reg-input'}
cedula_dict = {'class': 'font15 futura radius reg-input tooled', 'maxlength': '16'}

sexo_dict = {'class': 'reg-select futura'}
dia_dict = {'class': 'reg-sel-dia futura'}
mes_dict = {'class': 'reg-sel-mes futura'}
ano_dict = {'class': 'reg-sel-ano futura'}

celular_dict = {'class': 'font15 fleft futura radius reg-i-cell tooled fleft', 'maxlength': '10'}
tel_dict = {'class': 'font15 futura radius reg-input tooled nombre', 'maxlength': '7'}

depto_dict = {'id': 'departamento', 'class': 'reg-select radius futura'}
ciudad_dict = {'class': 'reg-select radius futura'}
op_movil_dict = {'class': 'reg-sel-operador futura'}
estrato_dict = {'class': 'reg-sel-operador futura  tooled'}
ocupacion_dict = {'class': 'reg-sel-operador futura  tooled'}

MES_CHOICE = (
    ('', 'Mes'),
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
    )
ESTRATO_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7')
    )

def convert_to_choice(agrega_null, list):
    lista = []
    if (agrega_null):
        lista = [("", '---------')]
    for elemnt in list:
        lista.append((elemnt.id, elemnt.nombre))
    return lista


def convert_to_choice_fechas(agrega_null, list, label):
    lista = []
    if (agrega_null):
        lista = [("", label)]
    for elemnt in list:
        lista.append((elemnt, elemnt))
    return lista


def convert_to_choice_numero(list):
    lista = [("", '- - - - - - - - -')]
    for elemnt in list:
        lista.append((elemnt.id, elemnt.numero))
    return lista


class LocationForm(forms.ModelForm):
    """
    Profile location form
    """

    class Meta:
        model = Profile
        fields = ('location', 'latitude', 'longitude', 'country')


class ProfileForm(forms.ModelForm):
    """
    Profile Form. Composed by all the Profile model fields.
    """

    def __init__(self, *args, **kwargs):
        self.reconfirmar = kwargs.pop('reconfirmar')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs["class"] = "none-input"
        self.fields['apellidos'].widget.attrs["class"] = "none-input"
        self.fields['direcion'].widget.attrs["class"] = "none-input"
        self.fields['telefono'].widget.attrs["class"] = "none-input"
        self.fields['celular'].widget.attrs["class"] = "none-input"
        self.fields['ciudad'].widget.attrs["class"] = "none-select2b ciudad"
        self.fields['departamento'].widget.attrs["class"] = "none-select2a pais"
        self.fields['operador_movil'].widget.attrs["class"] = "none-select2a pais"
        self.fields['sexo'].widget.attrs["class"] = "none-select"
        self.fields['ocupacion'].widget.attrs["class"] = "none-select"

        self.fields['estrato'].widget.attrs["class"] = "none-select"

        self.fields['estado_civil'].widget.attrs["class"] = "none-select"

        self.id = 0

        if 'reconfirmar' in  kwargs: #3 si la llave existe quiere decir que vamos a reconfirmar
            self.reconfirmar = True

        if not self.reconfirmar: # si el formulario es para reconfirmar el perfil
            exclude = ['fecha_de_nacimiento', 'cedula']

            for field_name in exclude:
                if field_name in self.fields:
                    del self.fields[field_name]
        else:
            self.fields['fecha_de_nacimiento'].widget.attrs["class"] = "none-input"
        instance = getattr(self, 'instance', None)

        if instance:
            self.id = instance.id

    estado_civil = forms.ModelChoiceField(EstadoCivil.objects.all().order_by('nombre'),
        widget=forms.Select(attrs=ocupacion_dict), required=True)

    ocupacion = forms.ModelChoiceField(Ocupacion.objects.all().order_by('nombre'),
        widget=forms.Select(attrs=ocupacion_dict), required=True)

    departamento = forms.ModelChoiceField(Departamento.objects.all().order_by('nombre'),
        widget=forms.Select(attrs={'id': 'id_departamento', 'class': 'reg-select radius futura'}), required=True)

    ciudad = forms.ModelChoiceField(Ciudad.objects.all(),
        widget=forms.Select(attrs={'class': 'reg-select radius futura', 'id': 'id_ciudad'}))
    operador_movil = forms.ModelChoiceField(OperadorMovil.objects.all(),
        widget=forms.Select(attrs={'class': 'reg-select radius futura'}))

    class Meta:
        model = Profile
        exclude = (
            'ideologiapolitica', 'escolaridad', 'orientacion', 'inviter_key', 'date', 'location',
            'latitude',
            'longitude', 'country',
            'user', 'public', 'saldo', 'edad', 'acerca_de_mi', 'pin_user', 'unsubscribe_counter', 'email_activo'
            )


    def clean_celular(self):
        """
        Verify that the username isn't already registered
        """
        celular = self.cleaned_data.get("celular")
        #if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
        lendigitos = len(str(celular))
        if lendigitos < 10:
            raise forms.ValidationError(
                _("Los numeros celulares en colombia como minimo tienen 10 digitos usted tiene :") + str(lendigitos))
        else:
            return celular


    def clean_telefono(self):
        """
        Verify that the username isn't already registered
        """
        telefono = self.cleaned_data.get("telefono")
        #if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
        lendigitos = len(str(telefono))
        if lendigitos < 5:
            raise forms.ValidationError(
                _("Los numeros fijos en colombia como minimo tienen 5  digitos usted tiene :") + str(lendigitos))
        else:
            return telefono


    def clean_estrato(self):
        estrato = self.cleaned_data.get("estrato")
        if not  estrato in range(1, 8, 1):
            raise forms.ValidationError(u"Por favor defina su estrato")
        return estrato

    def clean_sexo(self):
        sexo = self.cleaned_data.get("sexo")

        if sexo in ['', None]:
            raise forms.ValidationError(u"Por favor seleccione un genero")
        return sexo

    def clean_direcion(self):
        direcion = self.cleaned_data.get("direcion")
        if len(direcion) < 6:
            raise forms.ValidationError(u"Por favor especifique su dirección con mas precisión minimo 6 carateres")
        return direcion

    def clean_fecha_de_nacimiento(self):
        fecha_de_nacimiento = self.cleaned_data.get("fecha_de_nacimiento")
        if not self.reconfirmar:
            return fecha_de_nacimiento

        if fecha_de_nacimiento  in ["", None]:
            raise forms.ValidationError(
                u"Error en la fecha de nacimiento debe ser mayor de 18 años:  si su fecha de nacimiento esta mal sera eliminado de los sorteos ")

        dnacim = datetime.date(2012, 1, 1)
        dhoy = datetime.date.today()
        edad = relativedelta(dhoy, fecha_de_nacimiento).years
        if (edad < 18):
            raise forms.ValidationError(u"Error en la fecha de nacimiento debe ser mayor de 18 años:" + str(
                fecha_de_nacimiento) + u" si su fecha de nacimiento esta mal sera eliminado de los sorteos ")
        return fecha_de_nacimiento


    def clean_cedula(self):
        if self.reconfirmar:

            cedula = self.cleaned_data["cedula"]
            if len(str(cedula)) > 16:
                raise forms.ValidationError(_("Asegurese que el valor es menor o igual a 16 "))
            else:
                if not Profile.objects.filter(cedula=cedula).exclude(id=self.id).exists():
                    return cedula
                else:
                    raise forms.ValidationError(_("Esta cedula ya se encuentra registrada."))
        return self.cleaned_data["cedula"]

class PublicFieldsForm(forms.ModelForm):
    """
    Public Fields of the Profile Form. Composed by all the Profile model fields.
    """

    class Meta:
        model = Profile
        exclude = ('date', 'user', 'public')


class AvatarForm(forms.Form):
    """
    The avatar form requires only one image field.
    """
    photo = forms.FileField(required=False,max_length='10')
    url = forms.URLField(required=False)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url: return ''
        filename, headers = urllib.urlretrieve(url)
        if not mimetypes.guess_all_extensions(headers.get('Content-Type')):
            raise forms.ValidationError(_('The file type is invalid: %s' % type))
        return SimpleUploadedFile(filename, open(filename, 'rb').read(), content_type=headers.get('Content-Type'))

    def clean(self):

            #return imagen
        if not (self.cleaned_data.get('photo') or self.cleaned_data.get('url')):
            raise forms.ValidationError(_('You must enter one of the options'))
        return self.cleaned_data


class AvatarCropForm(forms.Form):
    """
    Crop dimensions form
    """
    top = forms.IntegerField()
    bottom = forms.IntegerField()
    left = forms.IntegerField()
    right = forms.IntegerField()

    def clean(self):
        if int(self.cleaned_data.get('right')) - int(self.cleaned_data.get('left')) < 96:
            raise forms.ValidationError(_("You must select a portion of the image with a minimum of 96x96 pixels."))
        else:
            return self.cleaned_data


class CheckboxSelectMultiple(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul style="display:none">']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_

    id_for_label = classmethod(id_for_label)


class FirstStepRegistrationForm(forms.Form):
    email1 = forms.EmailField(max_length=60, min_length=7, widget=forms.TextInput(attrs=attrs_dict), required=True,
        label=_("E-mail address"))
    email2 = forms.EmailField(max_length=60, min_length=7, widget=forms.TextInput(attrs=attrs_dict), required=True,
        label=_("E-mail address"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=_("Password"))
    tipo_referencia = forms.CharField(widget=forms.Select(attrs=sexo_dict,
        choices=convert_to_choice(True, TipoReferencia.objects.filter(activo=True))), label=_("tipo_referencia "),
        required=False)
    referencia = forms.ModelMultipleChoiceField(label="referencias", queryset=Referencia.objects.filter(activo=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'selector'}))
    tos = forms.BooleanField(required=True, label="Acepto terminos y condiciones")

    def clean_email1(self):
        """
        Verify that the email exists
        """
        self.cleaned_data["email1"] = self.cleaned_data["email1"].replace(" ", "").lower()
        email = self.cleaned_data.get("email1").replace(" ", "").lower()
        if not email: return  email

        try:
            User.objects.get(username=email)
            raise forms.ValidationError(u"Este correo ya existe inicia sesión.")
        except User.DoesNotExist:
            try:
                EmailValidation.objects.get(email=email)
                raise forms.ValidationError(u"Te enviamos un correo de validación a esta dirección revisa por favor.")
            except EmailValidation.DoesNotExist:
                return email.replace(" ", "").lower()
        return email

    def clean(self):
        """
        Verify that 2 emails fields are equal
        """
        if 'email1' in self.cleaned_data and 'email2' in self.cleaned_data:
            self.cleaned_data["email1"] = self.cleaned_data["email1"].replace(" ", "").lower()
            self.cleaned_data["email2"] = self.cleaned_data["email2"].replace(" ", "").lower()

            if self.cleaned_data['email1'] != self.cleaned_data['email2']:
                raise forms.ValidationError(_("Los Emails no coinciden."))
        return self.cleaned_data

    def clean_tos(self):
        tos = self.cleaned_data.get("tos")
        if tos:
            return tos
        else:
            raise forms.ValidationError(_("Debe Acceptar los Terminos y Condiciones."))
        return tos

    def save(self):
        username = self.cleaned_data.get('email1').replace(" ", "").lower()
        password = self.cleaned_data.get('password')
        referencias = self.cleaned_data.get('referencia')
        new_user = User.objects.create_user(username=username, email=username, password=password)
        new_user.is_active = settings.ACTIVAR_USUARIO
        new_user.save()
        nuevo_perfil = Perfil.objects.create(user=new_user)
        nuevo_perfil.set_inviter_key()
        if len(referencias) != 0:
            map(lambda referencia: nuevo_perfil.referencia.add(referencia), referencias)
        return nuevo_perfil

        ################################################################################


class SecondStepRegistrationForm(forms.Form):
    def listarciudades(self, ciudades):
        self.fields['ciudad'].choices = convert_to_choice(False, ciudades)
        return self

    nombre = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), required=True)
    apellidos = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), required=True)
    departamento = forms.ModelChoiceField(Departamento.objects.all().order_by('nombre'),
        widget=forms.Select(attrs=depto_dict), required=True)
    ciudad = forms.CharField(widget=forms.Select(attrs=ciudad_dict,
        choices=convert_to_choice(True, Ciudad.objects.get_ciudades_por_departamento(77091))), required=True)

    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"]
        if len(str(cedula)) > 16:
            raise forms.ValidationError(_("Asegurese que el valor es menor o igual a 16 "))
        else:
            if Profile.objects.filter(cedula=cedula).count() == 0:
                return cedula
            else:
                raise forms.ValidationError(_("Esta cedula ya se encuentra registrada."))
        return self.cleaned_data["cedula"]

    def save(self, perfil):
        nombre = self.cleaned_data.get('nombre')
        apellidos = self.cleaned_data.get('apellidos')
        departamento = self.cleaned_data.get('departamento')
        ciudad = Ciudad.objects.select_related().get(id=self.cleaned_data.get('ciudad'))
        region = ciudad.departamento.region

        perfil.nombre = nombre
        perfil.apellidos = apellidos = apellidos
        perfil.ciudad = ciudad
        perfil.departamento = departamento
        perfil.region = region
        perfil.save()

        ################################################################################


class ThirdStepRegistrationForm(forms.Form):
    sexo = forms.CharField(widget=forms.Select(attrs=sexo_dict, choices=convert_to_choice(True, Sexo.objects.all())),
        label=_("Sexo"), required=True)
    dia = forms.IntegerField(
        widget=forms.Select(attrs=dia_dict, choices=convert_to_choice_fechas(True, range(1, 32, 1), 'Dia')),
        label=_("Dia"), required=True)
    mes = forms.IntegerField(widget=forms.Select(attrs=mes_dict, choices=MES_CHOICE), label=_("Mes"), required=True)
    ano = forms.IntegerField(widget=forms.Select(attrs=ano_dict, choices=convert_to_choice_fechas(True,
        range(datetime.date.today().year - 90, datetime.date.today().year - 17, 1), u'Año')), label=_("Ano"),
        required=True)
    estado_civil = forms.CharField(
        widget=forms.Select(attrs=sexo_dict, choices=convert_to_choice(True, EstadoCivil.objects.all())),
        label=_("Estado Civil"), required=True)

    def clean(self):
        dia = self.cleaned_data.get("dia")
        mes = self.cleaned_data.get("mes")
        ano = self.cleaned_data.get("ano")
        if dia in [None, ''] or mes in [None, ''] or ano in [None, '']:
            self._errors["dia"] = self.error_class(["* Este campo es obligatorio"])
            raise forms.ValidationError("Este campo es obligatorio")
        if not(ano in ['', None])  or  not (mes in [None, ''] or not (dia in [None, '']) ):
            month, dias = calendar.monthrange(ano, mes)

            if (dia > dias):
                self._errors["dia"] = self.error_class(
                    ["El mes %s solo tiene %s dias y usted seleciono %s" % (mes, dias, dia)])
                raise forms.ValidationError(_("El mes %s solo tiene %s dias y usted seleciono %s" % (mes, dias, dia)))
        dnacim = datetime.date(ano, mes, dia)
        dhoy = datetime.date.today()
        edad = relativedelta(dhoy, dnacim).years
        if (edad < 18):
            self._errors["dia"] = self.error_class(["* EDAD MENOR A 18 REVISAR EL DIA"])
            self._errors["ano"] = self.error_class(["* EDAD MENOR A 18 REVISAR EL MES"])
            self._errors["mes"] = self.error_class(["* EDAD MENOR A 18 REVISAR EL AÑO"])
            raise forms.ValidationError(_(u"* La edad selecionada en la fecha es inferior a 18 años"))
        return self.cleaned_data

    def save(self, perfil):
        sexo = Sexo.objects.get(id=self.cleaned_data.get('sexo'))
        estado_civil = EstadoCivil.objects.get(id=self.cleaned_data.get('estado_civil'))
        ano = self.cleaned_data.get('ano')
        mes = self.cleaned_data.get('mes')
        dia = self.cleaned_data.get('dia')
        fecha_de_nacimiento = datetime.date(ano, mes, dia)
        perfil.fecha_de_nacimiento = fecha_de_nacimiento
        perfil.estado_civil = estado_civil
        perfil.sexo = sexo
        #perfil.ano = ano
        #perfil.mes = mes
        #perfil.dia = dia
        perfil.save()

        ################################################################################


class FourthStepRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FourthStepRegistrationForm, self).__init__(*args, **kwargs)
        self.id = 0

    def cargar_perfil(self, perfil):
        self.id = perfil.id



    def listarciudades(self, ciudades):
        self.fields['ciudad'].choices = convert_to_choice(False, ciudades)
        return self

    operador_movil = forms.CharField(
        widget=forms.Select(attrs=op_movil_dict, choices=convert_to_choice(True, OperadorMovil.objects.all())),
        label=_("Operador Movil"), required=True, error_messages={'required': 'El Operador es requerido'})
    telefono = forms.IntegerField(widget=forms.TextInput(attrs=tel_dict), required=True,
        error_messages={'required': 'El telefono es obligatorio'})
    celular = forms.IntegerField(widget=forms.TextInput(attrs=celular_dict), required=True)
    cedula = forms.IntegerField(widget=forms.TextInput(attrs=cedula_dict), label=_("Cedula"))

    ocupacion = forms.IntegerField(
        widget=forms.Select(attrs=ocupacion_dict, choices=convert_to_choice(True, Ocupacion.objects.all())),
        label=u"Ocupación", required=True, error_messages={'required': 'La ocupacion es requerida'})

    estrato = forms.CharField(
        widget=forms.Select(attrs=estrato_dict, choices=ESTRATO_CHOICES),
        label=_("Estrato"), required=True)

    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"]


        if len(str(cedula)) > 16:
            raise forms.ValidationError(_("Asegurese que el valor es menor o igual a 16 "))
        else:
            if not Profile.objects.filter(cedula=cedula).exclude(id=self.id).exists():
                return cedula
            else:
                raise forms.ValidationError(_("Esta cedula ya se encuentra registrada,vuelve a intentarlo."))
        return self.cleaned_data["cedula"]


    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]

        if len(str(telefono)) > 7:
            raise forms.ValidationError(_("Asegurese que el valor sea de 7 digitos"))

        #if telefono in [None,'']:
        #    self._errors["telefono"] = self.error_class([u"El telefono es obligatorio"])
        #    
        #del cleaned_data["telefono"]
        #    
        return self.cleaned_data["telefono"]

    def clean(self):
        tel_celular = len(str(self.cleaned_data.get("celular")))
        operador_movil = str(self.cleaned_data.get("operador_movil"))

        if tel_celular != 10 or operador_movil in [None, '']:
            if tel_celular in [None, '']:
                self._errors["celular"] = self.error_class(["El Celular es requerido obligatorio"])
            if tel_celular != 10:
                self._errors["celular"] = self.error_class(
                    ["El numero de caracteres es 10, ha escrito: %s" % (str(tel_celular))])
            if operador_movil in [None, '']:
                self._errors["operador_movil"] = self.error_class(["El Operador es requerido"])
            else:
                raise forms.ValidationError(" El celular y el operador son obligatorios ")
        return self.cleaned_data

    def save(self, perfil):
        operador_movil = OperadorMovil.objects.get(id=self.cleaned_data.get('operador_movil'))
        celular = self.cleaned_data.get('celular')
        ocupacion = Ocupacion.objects.get(id=self.cleaned_data.get('ocupacion'))
        telefono = self.cleaned_data.get('telefono')
        cedula = self.cleaned_data.get('cedula')
        perfil.operador_movil = operador_movil
        perfil.ocupacion = ocupacion
        perfil.celular = celular
        perfil.telefono = telefono
        perfil.cedula = cedula
        perfil.estrato = self.cleaned_data.get('estrato')

        perfil.save()
        EmailValidation.objects.add(user=perfil.user, email=perfil.user.email)

        ################################################################################

################################################################################
################################################################################
################################################################################
class RegistrationForm(forms.Form):
    def listarciudades(self, ciudades):
        self.fields['ciudad'].choices = convert_to_choice(False, ciudades)
        return self

        #truco
        #def clean_slug(self):
        #   return clean_unique(self, 'slug')
        #guillermo por favor definir los maxlength

    nombre = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), required=True)

    telefono = forms.RegexField(widget=forms.TextInput(attrs=tel_dict), error_message="Solo se permiten numeros enteros"
        , max_length=10, min_length=7, regex=r'[\d]+', required=True, )
    celular = forms.RegexField(widget=forms.TextInput(attrs=celular_dict),
        error_message="Solo se permiten numeros enteros", max_length=11, min_length=10, regex=r'[\d]+', required=True)

    apellidos = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), required=True)
    email = forms.EmailField(max_length=60, min_length=3, widget=forms.TextInput(attrs=attrs_dict), required=True,
        label=_("E-mail address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=_("Password (again)"))
    departamento = forms.ModelChoiceField(Departamento.objects.exclude(nombre='Todos'),
        widget=forms.Select(attrs=depto_dict), required=True)

    ciudad = forms.CharField(widget=forms.Select(attrs=sexo_dict,
        choices=convert_to_choice(True, Ciudad.objects.get_ciudades_por_departamento(77091))), required=True)

    tipo_referencia = forms.CharField(widget=forms.Select(attrs=sexo_dict,
        choices=convert_to_choice(True, TipoReferencia.objects.filter(activo=True))), label=_("tipo_referencia "),
        required=False)

    referencia = forms.ModelMultipleChoiceField(label="referencias", queryset=Referencia.objects.filter(activo=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'selector'}))
    #referencia = forms.ModelChoiceField(empty_label=None,label="referencias", queryset=Referencia.objects.filter(activo=True) , widget=CheckboxSelectMultiple())


    dia = forms.IntegerField(
        widget=forms.Select(attrs=dia_dict, choices=convert_to_choice_fechas(True, range(1, 32, 1), 'Dia')),
        label=_("Dia"), required=True)
    mes = forms.IntegerField(widget=forms.Select(attrs=mes_dict, choices=MES_CHOICE), label=_("Mes"), required=True)
    ano = forms.IntegerField(widget=forms.Select(attrs=ano_dict, choices=convert_to_choice_fechas(True,
        range(datetime.date.today().year - 90, datetime.date.today().year - 18, 1), u'Año')), label=_("Ano"),
        required=True)
    sexo = forms.CharField(widget=forms.Select(attrs=sexo_dict, choices=convert_to_choice(True, Sexo.objects.all())),
        label=_("Genero"), required=True)
    cedula = forms.RegexField(widget=forms.TextInput(attrs=cedula_dict), regex=r'[\d]+', max_length=16, min_length=5,
        label=_("Cedula"))
    tos = forms.BooleanField(required=True, label="Acepto terminos y condiciones")


    def clean_cedula(self):
        """
        Verify that the username isn't already registered
        """
        cedula = self.cleaned_data["cedula"]
        ##if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
        #if not set(cedula).issubset("0123456789"):
        #    raise forms.ValidationError(_("Solo se permiten numero en la cedula"))
        if Profile.objects.filter(cedula=cedula).count() == 0:
            return cedula
        else:
            raise forms.ValidationError(_("Esta cedula ya se encuentra registrada."))
        return self.cleaned_data["cedula"]

    #
    #    def clean_telefono(self):
    #        """
    #        Verify that the username isn't already registered
    #        """
    #        telefono = self.cleaned_data.get("telefono")
    #        #if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
    #        lendigitos=len(str(telefono ))
    #        if lendigitos<7:
    #            raise forms.ValidationError(_("Los numeros telefonicos en colombia como minimo tienen 7 digitos usted tiene :")+str(lendigitos))
    #        else:
    #            return telefono
    #    def clean_celular(self):
    #        """
    #        Verify that the username isn't already registered
    #        """
    #        celular = self.cleaned_data.get("celular")
    #        #if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
    #        lendigitos=len(str(celular))
    #        if lendigitos<10:
    #            raise forms.ValidationError(_("Los numeros de celular en colombia son de 10 digitos por favor retifique digito contados:")+str(lendigitos))
    #        else:
    #            return celular
    #===============================================================================





    def clean(self):
        """

        """
        dia = self.cleaned_data.get("dia")
        mes = self.cleaned_data.get("mes")
        ano = self.cleaned_data.get("ano")

        if dia in [None, '']:
            self._errors["dia"] = self.error_class(["* El dia es requerido"])
            raise forms.ValidationError("El dia es requerido")

        if mes in [None, '']:
            self._errors["mes"] = self.error_class(["* El mes  es requerido"])
            raise forms.ValidationError("El dia es requerido")

        if ano in [None, '']:
            self._errors["ano"] = self.error_class(["* El año es requerido"])
            raise forms.ValidationError("El dia es requerido")

        if not(ano in ['', None])  or  not (mes in [None, ''] or not (dia in [None, '']) ):
            month, dias = calendar.monthrange(ano, mes)

            if (dia > dias):
                self._errors["dia"] = self.error_class(
                    ["El mes %s solo tiene %s dias y usted seleciono %s" % (mes, dias, dia)])
                raise forms.ValidationError(_("El mes %s solo tiene %s dias y usted seleciono %s" % (mes, dias, dia)))

        dnacim = datetime.date(ano, mes, dia)
        dhoy = datetime.date.today()
        edad = relativedelta(dhoy, dnacim).years
        if (edad < 18):
            self._errors["dia"] = self.error_class(["* EDAD MENOR A 18 REVISAR EL DIA"])
            self._errors["ano"] = self.error_class(["* EDAD MENOR A 18 REVISAR EL MES"])
            self._errors["mes"] = self.error_class(["* EDAD MENOR A 18 REVISAR EL AÑO"])
            raise forms.ValidationError(_(u"* La edad selecionada en la fecha es inferior a 18 años"))

        """
        Verify that the 2 passwords fields are equal
        """
        if self.cleaned_data.get("password1") == self.cleaned_data.get("password2"):
            return self.cleaned_data
        else:
            raise forms.ValidationError(_("The passwords inserted are different."))
        return self.cleaned_data

    def clean_email(self):
        """
        Verify that the email exists
        """
        self.cleaned_data["email"] = self.cleaned_data["email"].replace(" ", "").lower()

        email = self.cleaned_data.get("email").replace(" ", "").lower()

        if not email: return  email

        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_("That e-mail is already used."))
        except User.DoesNotExist:
            try:
                EmailValidation.objects.get(email=email)
                raise forms.ValidationError(_("That e-mail is already being confirmed."))
            except EmailValidation.DoesNotExist:
                return email.replace(" ", "").lower()
        return email

    def clean_tos(self):
        tos = self.cleaned_data.get("tos")
        if tos:
            return tos
        else:
            raise forms.ValidationError(_("Debe Acceptar los Terminos y Condiciones."))
        return tos


class EmailValidationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        """
        Verify that the email exists
        """
        email = self.cleaned_data.get("email")
        if not (User.objects.filter(email=email) or EmailValidation.objects.filter(email=email)):
            return email

        raise forms.ValidationError(_("That e-mail is already used."))
