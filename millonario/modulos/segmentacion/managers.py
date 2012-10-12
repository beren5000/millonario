# -*- coding: utf-8 -*-
from django.db import models
class CiudadManager(models.Manager):
    
    def get_ciudades_por_departamento(self,id_departamento):
        return self.filter(departamento=id_departamento).order_by('nombre')

