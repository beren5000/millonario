# -*- coding: utf-8 -*-
from dateutil.relativedelta import *
from django.db.models import get_model
from django.utils.hashcompat import sha_constructor
from django.core.urlresolvers import reverse

from millonario.modulos.kernel.perfil.manager import  PerfilManager, PerfilManagerOptimizado
from millonario.modulos.kernel.userprofile.models import BaseProfile,Avatar
from millonario.modulos.segmentacion.models import *

from sorl.thumbnail import ImageField, get_thumbnail

import csv,codecs
import datetime
#from uuid import uuid4




ORIENTACION_CHOICES = (
                  ('G', ('Gay')), ('H', ('Hectero')),
                  ('I', ('Indefinido')),

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

class TipoReferencia(models.Model):
    nombre=models.CharField(max_length=100,unique=True, blank=False,null=False)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    imagen= ImageField(upload_to='referencias/tipo_referencia/', help_text="Imagen  o logo para el registro.",null=True,blank=True)
    activo=models.BooleanField(db_index=True,default=True)
    def __unicode__(self):
        return u'%s ' % (self.nombre)


class Referencia(models.Model):
    nombre=models.CharField(max_length=100,blank=False,null=False)
    tipo=models.ForeignKey(TipoReferencia,null=True,blank=True)
    imagen= ImageField(upload_to='referencias/patrocinadores/', help_text="Imagen  o logo para el registro.",null=True,blank=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)

    def __unicode__(self):
        return u'%s ' % (self.nombre)
        
    def mostrar_thumb(self,x,y):
        im = get_thumbnail(self.imagen, '%sx%s'%(x,y), crop='noop', quality=99,format='PNG')
        return (self.id,im.url)

    def mostrar_imagen(self):
        try:
            return '<a href="/admin/cliente/campana/%s/"><img src="%s"  /></a>'  % self.mostrar_thumb(50,50)
        except :
            return '<a href="/admin/cliente/campana/%s/">Imagen no disponible</a>'%  self.id

        #return '<a href="%s"><img src="%s"  /></a>'  %(self.id,self.imagen.url_50x50)
    mostrar_imagen.allow_tags = True


class Perfil(BaseProfile):
    nombre = models.CharField(max_length=255, blank=False,null=False)
    apellidos = models.CharField(max_length=255, blank=True,null=True)
    fecha_de_nacimiento = models.DateField(db_index=True,blank=True,null=True)
    direcion = models.CharField(max_length=255, null=True,blank=True)
    celular = models.BigIntegerField(db_index=True,null=True,blank=True)
    cedula = models.BigIntegerField(db_index=True,null=True,blank=True)
    telefono = models.BigIntegerField(null=True,blank=True)
    region = models.ForeignKey(Region,null=True,blank=True)
    departamento=models.ForeignKey(Departamento,null=True,blank=True)
    ciudad=models.ForeignKey(Ciudad,null=True,blank=True)
    area_metropolitana=models.ForeignKey(AreaMetropolitana,default=0,null=True,blank=True)
    sexo=models.ForeignKey(Sexo,blank=True,null=True)
    numero_de_accesos= models.IntegerField(default=0,null=True,blank=True)
    ######################
    edad=models.PositiveSmallIntegerField(db_index=True,default=0)
    acerca_de_mi = models.TextField(max_length=255,blank=True, null=True)
    barrio = models.CharField(max_length=255, blank=True,null=True)
    saldo= models.PositiveIntegerField(default=0,null=True,blank=True)
    orientacion = models.CharField(max_length=1, choices=ORIENTACION_CHOICES,default=1, blank=True,null=True)
    estrato = models.PositiveIntegerField(max_length=1, choices=ESTRATO_CHOICES, blank=True,null=True)
    ######### juego de azar  se activara en un futuro
    ######## perfiles para segmentacion de mercados ######
    ideologiapolitica=models.ForeignKey(IdeologiaPolitica,null=True,blank=True)
    religion=models.ForeignKey(Religion,null=True,blank=True)
    escolaridad=models.ForeignKey(Escolaridad,null=True,blank=True)
    ocupacion=models.ForeignKey(Ocupacion,null=True,blank=True)
    operador_movil=models.ForeignKey(OperadorMovil,null=True,blank=True)
    estado_civil=models.ForeignKey(EstadoCivil ,null=True,blank=True)
    activado_desde_facebook=models.BooleanField(default=False)
    perfil_completo=models.BooleanField(default=False)
    
    email_activo=models.BooleanField(db_index=True,default=True)
    referencia=models.ManyToManyField(Referencia,null=True,blank=True)

    objects=PerfilManager()
    objectsoptimo=PerfilManagerOptimizado()

    creado=models.DateTimeField(auto_now_add=True) # fecha de creacion
    modificado=models.DateTimeField(auto_now=True)# las_modify ultima modificacion
    inviter_key = models.CharField(max_length=70, null=True,blank=True, db_index=True)
    unsubscribe_counter = models.PositiveSmallIntegerField(default=0,null=True,blank=True)
    pin_bb = models.CharField(max_length=10, null=True,blank=True)


    # The date_range_filter attribute is used to identify which filterspec to apply.
    creado.date_range_filter = True
    # The first filter in the extra filter panel must explicitly include the stylesheet and javascript
    # for the calendar widgets to avoid having them displayed multiple times.
    creado.show_media = True
    def mostrar_thumb(self,x,y):
        from django.conf import  settings
        #return self.nombre+" " +self.apellidos
        if self.has_avatar():
            av = Avatar.objects.get(user=self.user, valid=True).image
            im = get_thumbnail(av, '%sx%s'%(x,y), crop='noop', quality=99,format='PNG')
            return im.url
        else:
            if self.sexo_id == 1:
                url = '%smedia_perfil/images/female_120.png' % settings.MEDIA_URL
            else:
                url = '%smedia_perfil/images/male_120.png' % settings.MEDIA_URL
            return url



    def mostrar_usuario(self):

        return '<a href="/seguimientos/auth/user/%s/" target="_blank" ><img src="%s" height=35  with=35  /></a>'  % (self.user.id,self.mostrar_thumb(35,35))
    mostrar_usuario.allow_tags = True
    def cambiar_clave(self):
        return '<a href="/seguimientos/perfil/perfil-clave/%s/" target="_parent" >Cedula Como clave </a>'  % (self.id)
    cambiar_clave.allow_tags = True

    def save(self, *args, **kwargs):
        self.region= self.departamento.region
        super(Perfil, self).save(*args, **kwargs)

    @property
    def dia(self):
        try:

            return self.creado.strftime("%A").decode('utf8', 'ignore')
        except:
            return "Indefinido"

    @property
    def hora(self):
        try:

            return self.creado.strftime("%H")
        except:
            return "-1"

    @property
    def minutos(self):
        try:
            return self.creado.strftime("%M")
        except:
            return "-1"

    @property
    def es_valido(self):
        return not (None in [self.sexo_id,self.region_id,self.edad])
    def __unicode__(self):
        return u'%s' % (self.nombre)
        
    class Meta:
        ordering = ['-creado','region' ,'edad','nombre']
        verbose_name = "Usuario Registrado"
        verbose_name_plural = "Usuarios registrados"

    @property
    def clicks_hijos(self):
        from django.db import connection

        cursor = connection.cursor()
        query="""SELECT IFNULL(sum(  ef.visitas )   , 0) clicks_hijos FROM inviter_contactsregister AS hijos
                LEFT OUTER JOIN  estadisticas_estadistica ee on ee.perfil_id=hijos.invite_profile_id
                LEFT OUTER JOIN  estadisticas_fechaxestadistica  ef on ef.estadistica_id=ee.id
                WHERE hijos.user_profile_id=%s"""

        cursor.execute(query, [self.id])
        row = cursor.fetchone()
        if row!=None:
            valor=row[0]
            return int  ( row[0] )
        return 0

    @property
    def fecha_registro(self):
        try:
            return self.creado.strftime("%Y/%m/%d")
        except:
            return "0/0/0"

    @property
    def hora_registro(self):
        try:
            return self.creado.strftime("%H:%M")
        except:
            return "-1:-1"

    @property
    def clicks_perfil(self):
        #clicks propios del usuario instacia
        from django.db import connection

        cursor = connection.cursor()
        query="""SELECT  IFNULL(sum(estadisticas_fechaxestadistica.visitas)   , 0)  clicks  FROM estadisticas_estadistica,estadisticas_fechaxestadistica, perfil_perfil

 WHERE estadisticas_estadistica.perfil_id = %s
 and perfil_perfil.id=estadisticas_estadistica.perfil_id
 and estadisticas_fechaxestadistica.estadistica_id=estadisticas_estadistica.id"""

        cursor.execute(query, [self.id])
        row = cursor.fetchone()
        if row!=None:

            return int  ( row[0] )
        return 0

    @property
    def clicks_nietos(self):
        from django.db import connection

        cursor = connection.cursor()
        query="""SELECT   IFNULL(sum(  ef.visitas )   , 0) clicks_nietos
FROM inviter_contactsregister hijos, inviter_contactsregister nietos
LEFT OUTER JOIN  estadisticas_estadistica ee on ee.perfil_id=nietos.invite_profile_id
LEFT OUTER JOIN  estadisticas_fechaxestadistica  ef on ef.estadistica_id=ee.id
WHERE hijos.user_profile_id=%s
AND nietos.user_profile_id=hijos.invite_profile_id"""

        cursor.execute(query, [self.id])
        row = cursor.fetchone()
        if row!=None:
            valor=row[0]
            return int  ( row[0] )
        return 0

    @property
    def get_all_hijos(self):
        # si usted usa este metodo este metodo tiene un atributo llamado click que calcula de manera eficiente los clicks
        # no use clicks_nietos o clicks_hijos
        return Perfil.objects.get_hijos(self.id)
    @property
    def usuarios_invitados(self):
        return self.get_all_hijos

    @property
    def get_all_nietos(self):
        # si usted usa este metodo este metodo tiene un atributo llamado click que calcula de manera eficiente los clicks
        # no use clicks_nietos o clicks_hijos

        return Perfil.objects.get_nietos(self.id)


    @property
    def puntos_padre(self):
        return self.clicks_perfil*5

    @property
    def puntos_hijos(self):
        return self.clicks_hijos*3

    @property
    def puntos_nietos(self):
        return self.clicks_nietos*2

    @property
    def get_full_name(self):
        #return self.nombre+" " +self.apellidos
        try:
            return u'%s %s' %(self.nombre, self.apellidos)
        except:
            return u'RECUERDE INGRESAR SU NOMBRE  Y APELLIDOS ES VITAL PARA RECLAMAR'

    @property
    def nombres_apellidos(self):
        # solo para que se vea bien la columna en el admin
        return self.get_full_name

    def save(self, *args, **kwargs):
        if not self.ciudad in ['',None]:
            if not self.ciudad.area_metropolitana in ['',None]:
                self.area_metropolitana=self.ciudad.area_metropolitana
        if not  (self.fecha_de_nacimiento in [None, '']):
            dnacim = datetime.date(self.fecha_de_nacimiento.year, self.fecha_de_nacimiento.month, self.fecha_de_nacimiento.day)
            dhoy = datetime.date.today()
            edad = relativedelta(dhoy, dnacim)
            #if (dhoy.month>=dnacim.month):
            #    edad=dhoy.year-dnacim.year
            #else:
            #    edad=dhoy.year-dnacim.year-1
            self.edad = edad.years
        super(Perfil, self).save(*args, **kwargs)

    @property
    def age(self):
        #print "\a"
        if not (self.edad in [None, '']):
            print "\a"
            return self.edad
        if not  (self.fecha_de_nacimiento in [None, '']):
            #print "\a"
            dnacim = datetime.date(self.fecha_de_nacimiento.year, self.fecha_de_nacimiento.month, self.fecha_de_nacimiento.day)
            dhoy = datetime.date.today()
            edad = relativedelta(dhoy, dnacim)
            #if (dhoy.month>=dnacim.month):
            #    edad=dhoy.year-dnacim.year
            #else:
            #    edad=dhoy.year-dnacim.year-1
            #self.edad =abs( edad.years)
            #elf.save()
            return edad.years
        else:
            #print "\a"
            return 0


    def segundo_paso_imcompleto(self):
        if self.apellidos is None or self.departamento is None or self.ciudad is None :
            return True
        else:
            return False
    def tercer_paso_imcompleto(self):
        if self.estado_civil is None or self.sexo is None or self.fecha_de_nacimiento is None:
            return True
        else:
            return False
    def cuarto_paso_imcompleto(self):
        if self.operador_movil is None or self.telefono is None or self.celular is None or self.cedula is None:
            return True
        else:
            return False
        
        
    
        
class ProcesarEmailBounce(models.Model):
                  
    csv_file= models.FileField (upload_to='emails/bouncers/', help_text="cargue el csv", blank=True, null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)

    def csv_file_path(self):        
        return self.csv_file.path
    csv_file_path.allow_tags = True             

    
    def procesar_csv(self):
        stream_reader = csv.reader(open(self.csv_file.path, 'rb'), delimiter=';', quotechar='|')
        encoder = codecs.getincrementalencoder("latin-1")()
        
        next(stream_reader)
        for row in stream_reader:
                  print row
                  if len(row)!=0:
                      procesar_bouncer,tipo_de_error,correo_eletronico,razon,total_devueltos=self,row[0],row[1],row[2],int(row[3])
                      email_bouncer=EmailBounce()
                      email_bouncer.tipo_de_error=unicode(tipo_de_error, 'utf-8', 'ignore')  
                      email_bouncer.correo_eletronico=unicode(correo_eletronico, 'utf-8', 'ignore')  
                      email_bouncer.razon = unicode(razon, 'utf-8', 'ignore') 
                      
                      email_bouncer.total_devueltos=total_devueltos                  
                      email_bouncer.procesar_bouncer=procesar_bouncer
                      email_bouncer.save()
                  
                  
                  
                  
    def save(self, *args, **kwargs):
             
        super(ProcesarEmailBounce, self).save(*args, **kwargs)
        self.procesar_csv()  

##clase para lo relacionado con el bounce mail
##en esta clase se encontrara la tabla con los emails de envio vetado
class EmailBounce(models.Model):
      tipo_de_error =  models.CharField(max_length=255, blank=False,null=False)
      correo_eletronico = models.EmailField(default="@host.com",blank=True,null=True, db_index=True)
      razon =  models.CharField(max_length=255, blank=False,null=False)
      total_devueltos = models.PositiveIntegerField(db_index=True,null=True,blank=True)
      creado=models.DateTimeField(auto_now_add=True)
      modificado=models.DateTimeField(auto_now=True)
      procesar_bouncer=models.ForeignKey(ProcesarEmailBounce,null=True,blank=True)
      #def proc_email(self):
      #    print "Procesando correos... por favor espere"
      #    csv_dir=settings.EMAILBOUNCE_DIRS # Directorio en el que se encuentra el o los archivos csv a procesar
      #    os.chdir(csv_dir) #entro al directorio
      #    lista = os.listdir('.')#listo todos los archivos de ese directorio
      #    for i in lista:        #por cada archivo del directorio
      #        try:               #intento
      #            tmp=i
      #            i=i.split('.') #separar el nombre del archivo de su extension
      #            if i[0][0:3]!='pro' and i[1]=='csv': #si el nombre del archivo empieza con pro, y es csv
      #                   cs=open(i, 'rb')#abro el archivo
      #                   next(cs)               #le quito la cabecera
      #                   for row in cs:        #por cada linea del csv
      #                       row=row.rstrip()  #remuevo el end of line
      #                       row=row.split(';')   #obtengo la linea y la separo por comas
      #                       ##se averigua si existe el correo a insertar
      #                       exist=self.objects.filter(correo_eletronico=str(row[1])).count()
      #                       if exist==0:
      #                          #####inserto cada uno de los campos
      #                          self.tipo_de_error.save(str(row[0]))
      #                          self.correo_electronico.save(str(row[1]))
      #                          self.razon.save(str(row[2]))
      #                          self.total_devueltos.save(int(row[3]))
      #                       else:
      #                          #o actualizo solo el campo necesario
      #                          self.objects.filter(correo_eletronico=str(row[1])).update(total_devueltos=int(row[3]))
      #                   f.close()#cierro el archivo
      #            os.rename(tmp,'procesado_'+str(datetime.datetime.now()))#renombro ese archivo como procesado      
      #        except:
      #            pass
      #    print "csv's procesados"
class VisitasReferenciasFecha(models.Model):
    referencia = models.ForeignKey(Referencia,null=True,blank=True)
    fecha_registro = models.DateField(db_index=True,blank=True,null=True)
    tipo_referencia = models.CharField(max_length=300)
    
    cantidad = models.IntegerField()
    region = models.ForeignKey(Region,null=True,blank=True)
    departamento=models.ForeignKey(Departamento,null=True,blank=True)
    ciudad=models.ForeignKey(Ciudad,null=True,blank=True)
    sexo=models.ForeignKey(Sexo,blank=True,null=True)

    class Meta:
        db_table = u'VISITAS_REFERENCIAS_FECHA'
        ordering = ['-cantidad', 'referencia','fecha_registro']
        verbose_name = "Como te enteraste dia a dia"
        verbose_name_plural = "Como te enteraste dia a dia"

    @property
    def cantidad_registros(self):
        return str(self.cantidad)


    @property
    def hora_registro(self):
        try:
            return self.fecha_registro.strftime("%H:%M")
        except:
            return "-1:-1"
class TopPerfilesInvitados(models.Model):
    invitados = models.IntegerField()
    invitados_efectivos = models.BigIntegerField(null=True, blank=True)
    creado = models.DateField(db_index=True,blank=True,null=True)
    nombre = models.CharField(max_length=765)
    apellidos = models.CharField(max_length=765, blank=True)
    region = models.ForeignKey(Region,null=True,blank=True)
    departamento=models.ForeignKey(Departamento,null=True,blank=True)
    ciudad=models.ForeignKey(Ciudad,null=True,blank=True)
    sexo=models.ForeignKey(Sexo,blank=True,null=True)
    correo = models.CharField(max_length=768)

    class Meta:
        db_table = u'TOP_PERFILES_INVITADOS'
        ordering = [ '-invitados']
        verbose_name = "Estadistica de usuarios invitados"
        verbose_name_plural = "Estadistica de usuarios invitados"
   
        
class SistemaDePuntos(models.Model):
    perfil = models.ForeignKey(Perfil)
    puntos = models.BigIntegerField(null=True,blank=True)
    clickero = models.BooleanField(default=False,blank=True)
    puntos_adicionales = models.BigIntegerField(null=True,blank=True,default=0)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)


    def numero_hijos(self):
        ContactsRegister = get_model('inviter', 'ContactsRegister')
        num_mishijos=ContactsRegister.objects.filter(user_profile=self.perfil).count()
        return num_mishijos

    @property
    def cedula(self):
        return self.perfil.cedula

    @property
    def correo(self):
        return self.perfil.user.email

    @property
    def ciudad(self):
        return self.perfil.ciudad.nombre

    @property
    def departamento(self):
        return self.perfil.departamento.nombre
    @property
    def nombre_completo(self):
        return self.perfil.nombres_apellidos


    @property
    def clicks_hijos(self):
        from django.db import connection

        cursor = connection.cursor()
        query="""SELECT IFNULL(sum(  perfil_sistemadepuntos.puntos )   , 0) clicks_hijos FROM inviter_contactsregister,perfil_sistemadepuntos					
WHERE inviter_contactsregister.invite_profile_id=perfil_sistemadepuntos.perfil_id
and inviter_contactsregister.user_profile_id=%s"""

        cursor.execute(query, [self.perfil_id])
        row = cursor.fetchone()
        if row!=None:
            valor=row[0]
            return int  ( row[0] )
        return 0
    
    @property
    def clicks_nietos(self):
        from django.db import connection

        cursor = connection.cursor()
        query=""" SELECT   IFNULL(sum(  perfil_sistemadepuntos.puntos )   , 0) clicks_nietos
FROM inviter_contactsregister hijos, inviter_contactsregister nietos,  perfil_sistemadepuntos 
where
hijos.user_profile_id=%s
AND nietos.user_profile_id=hijos.invite_profile_id
and perfil_sistemadepuntos.perfil_id=nietos.invite_profile_id"""

        cursor.execute(query, [self.perfil_id])
        row = cursor.fetchone()
        if row!=None:
            valor=row[0]
            return int  ( row[0] )
        return 0

    @property
    def get_all_hijos(self):
        # si usted usa este metodo este metodo tiene un atributo llamado click que calcula de manera eficiente los clicks
        # no use clicks_nietos o clicks_hijos
        return Perfil.objects.get_hijos(self.id)
    
    @property
    def get_all_nietos(self):
        # si usted usa este metodo este metodo tiene un atributo llamado click que calcula de manera eficiente los clicks
        # no use clicks_nietos o clicks_hijos

        return Perfil.objects.get_nietos(self.id)

    @property
    def puntos_padre(self):
        if self.puntos:
            return self.puntos*5
        return 0

    @property
    def puntos_hijos(self):
        return self.clicks_hijos*3

    @property
    def puntos_nietos(self):
        return self.clicks_nietos*2
    
    @property
    def mis_puntos(self):
        if self.puntos_adicionales != None:
           return self.puntos_padre + self.puntos_hijos + self.puntos_nietos + self.puntos_adicionales
        else:
           return self.puntos_padre + self.puntos_hijos + self.puntos_nietos + 0       
 
    class Meta:
        ordering = ['-puntos']
        verbose_name = "Sistema de puntos"
        verbose_name_plural = "Sistemas de puntos"