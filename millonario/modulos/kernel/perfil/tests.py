__author__ = 'juan'
from django.db.models import Q
from django.utils import unittest
from millonario.modulos.kernel.perfil.models import  Perfil


__author__ = 'juan'
from django.db.models import Q
from django.utils import unittest
import random
from django.contrib.auth.models import User
from django.test.client import Client

class PerfilTestCase(unittest.TestCase):
    def setUp(self):
        self.perfiles= Perfil.objects.all()
        self.usuarios=[]
        self.client = Client()
        for i in range(0,5):
            username = str(random.random())+str(i)+"prueba@prueba.com"
            password = username
            newuser = User.objects.create_user(username=username, email=username, password=password)
            self.usuarios.append(newuser)
        
    def testlogin(self):
        "PROBANDO LINKS."
        for usuario in self.usuarios:
            response = self.client.get('/registro-demo-second-step/')
            login= self.client.login(username=usuario.username, password=usuario.username)            
            print login,self.assertTrue(login)
            usuario.delete()


    def validando_puntos(self):
        for perfil in self.perfiles:
            print perfil, perfil.id, "clicks nietos %s"%perfil.clicks_nietos,"clicks hijos %s"%perfil.clicks_hijos,"clicks perfil %s"%perfil.clicks_perfil

    def validando_hijos(self):
        for perfil in self.perfiles:
            print "se van a validar los hijos de ",perfil, perfil.id,"clicks perfil %s"%perfil.clicks_perfil
            hijos=perfil.get_all_hijos
            i=0
            for hijo in hijos:
                i=1
                print "mostrando los hijos de ",perfil," hijo %s"%hijo," hijo id %s"%hijo.id, "clicks nietos %s"%hijo.clicks_nietos,"clicks hijos %s"%hijo.clicks_hijos
            if (i!=0):
                print "\n\n ...."

    def validando_nietos(self):
        for perfil in self.perfiles:
            print "se van a validar los nietos de ",perfil, perfil.id,"clicks perfil %s"%perfil.clicks_perfil
            nietos=perfil.get_all_nietos
            i=0 
            for nieto  in nietos:
                i=1
                print "mostrando los nietos de ",perfil,"  nieto : ",nieto ," nieto id:%s"%nieto.id, "clicks nietos %s"%nieto.clicks_nietos,"clicks hijos %s"%nieto.clicks_hijos
            if (i!=0):
                print "\n\n ...."

