# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import force_str
from django.db import models
from datetime import date 

# Create your models here.
class Verbotipo(models.Model):
    verbotipo = models.CharField(max_length=64,null=True)
    verbotiposeq=models.IntegerField(null=True)

    def __str__(self):
        return self.verbotipo

class Verbo(models.Model):
    verbo = models.CharField(max_length=32)
    tipo=models.ForeignKey(Verbotipo,on_delete=models.SET_NULL,related_name="tipo_v",null=True)
    
    def __str__(self):
        return self.verbo

class Pronombre(models.Model):
    pronombre=models.CharField(max_length=8)
    pronombreseq=models.IntegerField(null=True)

    def __str__(self):
        return self.pronombre


class Tiempo(models.Model):
    tiempo=models.CharField(max_length=30)
    tiemposeq=models.IntegerField(null=True)

    def __str__(self):
        return self.tiempo

class Level(models.Model):
    level=models.CharField(max_length=5)

    def __str__(self):
        return self.level 


class Conjugacion(models.Model):
    verbo=models.ForeignKey(Verbo,on_delete=models.CASCADE,related_name="conjugacions")
    tiempo=models.ForeignKey(Tiempo,on_delete=models.CASCADE,related_name="tiempo_c")
    pronombre=models.ForeignKey(Pronombre,on_delete=models.CASCADE,related_name="pronombre_c")
    conjugacion=models.CharField(max_length=30)
    level=models.ForeignKey(Level,on_delete=models.CASCADE,related_name="conjugacion")
    
    def __str__(self):
#        conj  = self.conjugacion + " : " + self.verbo + " - " + self.tiempo + " - " + self.pronombre 
        return self.conjugacion




class Palabratipo(models.Model):
    palabratipo = models.CharField(max_length=32,null=True)
    def __str__(self):
        return self.palabratipo

class Palabrafecha(models.Model):
    palabrafecha = models.DateTimeField(null=True,default=date.today)
    def __str__(self):
        return str(self.palabrafecha)

class Palabragenero(models.Model):
    palabragenero = models.CharField(max_length=2,null=True)
    def __str__(self):
        return str(self.palabragenero)

class Palabranivel(models.Model):
    palabranivel = models.CharField(max_length=2,null=True)

    def __str__(self):
        return self.palabranivel

class Palabrafamilia(models.Model):
    palabrafamilia = models.CharField(max_length=30,null=True)
    palabrafamiliaseq=models.IntegerField(null=True)

    def __str__(self):
        return self.palabrafamilia

class Palabra(models.Model):
    palabrafecha= models.ForeignKey(Palabrafecha,on_delete=models.CASCADE,related_name="palabra") 
    palabra = models.CharField(max_length=40,null=True)
    traduccion = models.CharField(max_length=60,null=True)
    palabranivel = models.ForeignKey(Palabranivel,on_delete=models.CASCADE,related_name="palabra")
    palabratipo = models.ForeignKey(Palabratipo,on_delete=models.CASCADE,related_name="palabra")
    palabragenero = models.ForeignKey(Palabragenero,on_delete=models.CASCADE,related_name="palabra")
    palabrafamilia = models.ForeignKey(Palabrafamilia,on_delete=models.CASCADE,related_name="palabra")

    def __str__(self):
        return self.palabra

