# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import force_str
from django.db import models


# Create your models here.
class Verbotipo(models.Model):
    verbotipo = models.CharField(max_length=64,null=True)

    def __str__(self):
        return self.verbotipo

class Verbo(models.Model):
    verbo = models.CharField(max_length=32)
    tipo=models.ForeignKey(Verbotipo,on_delete=models.SET_NULL,related_name="tipo_v",null=True)
    
    def __str__(self):
        return self.verbo

class Pronombre(models.Model):
    pronombre=models.CharField(max_length=8)

    def __str__(self):
        return self.pronombre


class Tiempo(models.Model):
    tiempo=models.CharField(max_length=30)

    def __str__(self):
        return self.tiempo

class Conjugacion(models.Model):
    verbo=models.ForeignKey(Verbo,on_delete=models.CASCADE,related_name="conjugacions")
    tiempo=models.ForeignKey(Tiempo,on_delete=models.CASCADE,related_name="tiempo_c")
    pronombre=models.ForeignKey(Pronombre,on_delete=models.CASCADE,related_name="pronombre_c")
    conjugacion=models.CharField(max_length=30)
    level=models.IntegerField(default=0)
    
    def __str__(self):
#        conj  = self.conjugacion + " : " + self.verbo + " - " + self.tiempo + " - " + self.pronombre 
        return self.conjugacion
