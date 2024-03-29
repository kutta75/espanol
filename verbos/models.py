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
    pronombre=models.CharField(max_length=13)
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

class Sub_modelo(models.Model):
    sub_modelo= models.CharField(max_length=30,null=True)
    sub_modelo_seq=models.IntegerField(null=True)
    def __str__(self):
        return self.sub_modelo

class Sub_conj(models.Model):
    sub_conj= models.CharField(max_length=30,null=True)
    sub_conj_modelo=models.ManyToManyField(Sub_modelo)
    def __str__(self):
        return self.sub_conj

# table des principales qui introduiront les conjonctions  + subordonnée à un temps adhoc
# la principale pourra ete au present ou au passé et le temps à utiliser est specifié dans sub_tiempo 
class Sub_princ(models.Model): 
    sub_princ=models.CharField(max_length=60,null=True)
    sub_princ_seq=models.IntegerField(null=True)
    sub_modelo=models.ForeignKey(Sub_modelo,on_delete=models.CASCADE,related_name="sub_princ")
    sub_tiempo_seq=models.IntegerField(null=True)
    def __str__(self):
        return self.sub_princ
