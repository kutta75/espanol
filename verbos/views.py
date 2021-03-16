from django.shortcuts import render
import random 
from verbos.models import Verbo,Tiempo,Conjugacion,Pronombre,Verbotipo

# Create your views here.
def index(request):
    verbos = Verbo.objects.all()
    tiempos = Tiempo.objects.all()
    pronombres = Pronombre.objects.all()
    context= { 
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres
            }
    return render(request,"verbos/index.html",context)

def verbo(request,verbo_id):
    verbo= Verbo.objects.get(pk=verbo_id)
    context = { 
            "verbo" : verbo ,
            "conjugacions" : verbo.conjugacions.all().order_by('tiempo')
            }
    return render(request,"verbos/verbo.html",context)

def conjugacion(request): 
    conjugacion=Conjugacion.objects.filter(verbo_id='5')
    context = { 
            "conjugacion" : conjugacion
            }
    return render(request,"verbos/conjugacion.html",context)

def verbos(request):
    verbos = Verbo.objects.all()
    tiempos = Tiempo.objects.all()
    pronombres = Pronombre.objects.all()
    context= { 
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres
            }
    return render(request,"verbos/verbos.html",context)

def verbos_exo(request,conjugacion_id):
    resuelto = " sabes tus conjugaciones ? "
    trace= " trace "
    if request.method=="POST":
# traitement de la reponse apportée en comparant avec la question posée
        respuesta= request.POST.getlist('respuesta')
        conjugacion = Conjugacion.objects.get(pk=conjugacion_id)
        trace = str(conjugacion.conjugacion)  + str(respuesta[0]) 
        if respuesta[0] == conjugacion.conjugacion:
            resuelto="exito"
        else:
            resuelto="fracasso"

# preparation de la question suivante en exploit:ant les criteres de selection pour trouver une nouvelle conjugaion aleatoirement 
        tiempos_selected= request.POST.getlist('tiempos_selected')
        tiempos_checked= {}
        for tiempo_selected in tiempos_selected :
            tiempos_checked[tiempo_selected]="checked"
    else:
        tiempos_checked={"start":"go"}
    verbos = Verbo.objects.all()
    tiempos = Tiempo.objects.all()
    if request.method=="POST":
        for tiempo in tiempos:
            if str(tiempo.id) in tiempos_selected :
                tiempo.checked="checked"
            else:
                tiempo.checked="unchecked"
    pronombres = Pronombre.objects.all() 
    levels = Verbo.objects.all()
    verbotipos = Verbotipo.objects.all()
    if request.method=="POST":
        conjugacion_selectada_count =Conjugacion.objects.filter(tiempo__in=tiempos_selected).count()
        if conjugacion_selectada_count > 0:  
            conjugacion_selectada=Conjugacion.objects.filter(tiempo__in=tiempos_selected)
            loto = []
            for conjugacion in conjugacion_selectada:
                loto.append(conjugacion.pk)
            loto_winner=random.randint(0,conjugacion_selectada_count-1)
            pk_winner=loto[loto_winner]
        else:
            loto_winner=0
            pk_winner=1
        conjugacion_selectada=Conjugacion.objects.get(pk=pk_winner)
    else:
        conjugacion_selectada=Conjugacion.objects.first()
        conjugacion_selectada_count =Conjugacion.objects.all().count()
        pk_winner=0
        loto_winner=0
       
    context= { 
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres,
            "levels" : levels,
            "verbotipos" : verbotipos,
            "tiempos_checked": tiempos_checked,
            "conjugacion_selectada" : conjugacion_selectada,
            "conjugacion_selectada_count" : conjugacion_selectada_count,
            "loto_winner" : loto_winner,
            "pk_winner" : pk_winner,
            "resuelto" : resuelto,
            "trace" : trace
            }
    return render(request,"verbos/verbos_exo.html",context)


def palabras(request,id1,id2):
    context= {
            "id1" : id1,
            "id2" : id2
            }

    return render(request,"verbos/palabras.html",context)


