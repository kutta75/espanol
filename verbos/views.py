from django.shortcuts import render
import random,json  
from django.forms.models import model_to_dict 
from verbos.models import Verbo,Tiempo,Conjugacion,Pronombre,Verbotipo,Level,Palabra,Palabratipo,Palabragenero,Palabranivel,Palabrafamilia,Palabrafecha


def jslist(myqueryset):
    jstname=myqueryset.model.__name__
    jstlst=[]
    for item in myqueryset:
        jstlst.append([jstname,item.id])
    return jstlst

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
            "conjugacions" : verbo.conjugacions.all().order_by('tiempo__tiemposeq')
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






def verbos_exo(request,mode_id,conjugacion_id):
    resuelto = " sabes tus conjugaciones ? "
    trace= "<= puedes utilizar estas lettras"
    tracerep= "  "
    trace_id= "  "
    if request.method=="POST":
        if mode_id==1:
# traitement de la reponse apportée i a la question rang n-1 en comparant avec la question posée rand n-1 dont on connait l'idi du verbe qui a servi à la question 
            respuesta= request.POST.getlist('respuesta')
            conjugacion = Conjugacion.objects.get(pk=conjugacion_id)
            # preparation du texte à afficher pour présenter la bonne reponse 
            trace = str(conjugacion.tiempo) + " " + str(conjugacion.verbo) + " " + str(conjugacion.pronombre) +" " + str(conjugacion.conjugacion)   
            tracerep =  str(respuesta[0]) 
            trace_id =  str(conjugacion.id) 
            # nettoyage des espaces qui pourraient etre dans les 2 chaines 
            if respuesta[0].replace(" ","") == conjugacion.conjugacion.replace(" ",""):
                resuelto="1"
            else:
                resuelto="0"

# preparation de la question suivante en exploitant les criteres de selection pour trouver une nouvelle conjugaion aleatoirement 
# recuperation des filtres selectionnés 
        verbotipos_selected= request.POST.getlist('verbotipo')
        pronombres_selected= request.POST.getlist('pronombre')
        tiempos_selected= request.POST.getlist('tiempo')
        levels_selected= request.POST.getlist('level')
        tiempos_checked= {}
        pronombres_checked= {}
        verbotipos_checked= {}
        levels_checked= {}
        for tiempo_selected in tiempos_selected :
            tiempos_checked[tiempo_selected]="checked"
        for pronombre_selected in pronombres_selected :
            pronombres_checked[pronombre_selected]="checked"
        for verbotipo_selected in verbotipos_selected :
            verbotipos_checked[verbotipo_selected]="checked"
        for level_selected in levels_selected :
            levels_checked[level_selected]="checked"
    else:
        tiempos_checked={"start":"go"}
        pronombres_checked= {}
        verbotipos_checked= {}
        levels_checked= {}
    verbos = Verbo.objects.all()
    tiempos = Tiempo.objects.all().order_by('tiemposeq')
    pronombres = Pronombre.objects.all().order_by('pronombreseq') 
    verbotipos = Verbotipo.objects.all()
    levels = Level.objects.all()

    if request.method=="POST":
        for tiempo in tiempos:
            if str(tiempo.id) in tiempos_selected :
                tiempo.checked="checked"
            else:
                tiempo.checked="unchecked"
        for pronombre in pronombres:
            if str(pronombre.id) in pronombres_selected :
                pronombre.checked="checked"
            else:
                pronombre.checked="unchecked"
        for verbotipo in verbotipos:
            if str(verbotipo.id) in verbotipos_selected :
                verbotipo.checked="checked"
            else:
                verbotipo.checked="unchecked"
        for level in levels:
            if str(level.id) in levels_selected :
                level.checked="checked"
            else:
                level.checked="unchecked"

    if request.method=="POST":
        
        conjugacion_selectada_count =Conjugacion.objects.filter(tiempo__in=tiempos_selected).filter(pronombre__in=pronombres_selected).filter(verbo__in=Verbo.objects.filter(tipo__in=verbotipos_selected)).filter(level__in=levels_selected).count()
        if conjugacion_selectada_count > 0:  
            conjugacion_selectada=Conjugacion.objects.filter(tiempo__in=tiempos_selected).filter(pronombre__in=pronombres_selected).filter(verbo__in=Verbo.objects.filter(tipo__in=verbotipos_selected)).filter(level__in=levels_selected)
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
    # myset set à porter la liste des objets qui servent à faire des  filtres pour les exo 
    myset=("tiempos","pronombres","verbotipos")

    jstiempos=jslist(tiempos)
    jspronombres=jslist(pronombres)
    jsverbotipos=jslist(verbotipos)
    jslevels=jslist(levels)
    context= { 
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres,
            "levels" : levels,
            "verbotipos" : verbotipos,
            "tiempos_checked": tiempos_checked,
            "verbotipos_checked": verbotipos_checked,
            "pronombres_checked": pronombres_checked,
            "conjugacion_selectada" : conjugacion_selectada,
            "conjugacion_selectada_count" : conjugacion_selectada_count,
            "loto_winner" : loto_winner,
            "pk_winner" : pk_winner,
            "resuelto" : resuelto,
            "trace" : trace,
            "trace_id" : trace_id,
            "tracerep" : tracerep,
            "myset" : myset,
            "jstiempos" : jstiempos,
            "jsverbotipos" : jsverbotipos,
            "jslevels": jslevels,
            "jspronombres" : jspronombres
            }
    return render(request,"verbos/verbos_exo.html",context)

def palabra(request):
    # fonction pour exervice sur les palabras 
    familias  = Palabrafamilia.objects.all()
    tipos =     Palabratipo.objects.all()
    generos =   Palabragenero.objects.all()
    nivels =    Palabranivel.objects.all() 
    fechas =    Palabrafecha.objects.all().order_by('palabrafecha') 
    # myset set à porter la liste des objets qui servent à faire des  filtres pour les exo 
    jsfamilias=jslist(familias)
    jsgeneros=jslist(generos)
    jsnivels=jslist(nivels)
    context= {
            "familias" : familias,
            "tipos" : tipos,
            "generos" : generos,
            "nivels" : nivels , 
            "fechas" : fechas,
        }
    return render(request,"verbos/palabra.html",context) 


def palabras(request,id1,id2):
# fonction pour tester 
    verbos = Verbo.objects.all()
    tiempos = Tiempo.objects.all()
    pronombres = Pronombre.objects.all() 
    verbotipos = Verbotipo.objects.all()
    # myset set à porter la liste des objets qui servent à faire des  filtres pour les exo 
    myset=(tiempos,pronombres,verbotipos)
    jstiempos=jslist(tiempos)
    jspronombres=jslist(pronombres)
    jsverbotipos=jslist(verbotipos)
    context= {
            "id1" : id1,
            "id2" : id2,
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres,
            "verbotipos" : verbotipos,
            "myset" : myset,
            "jstiempos" : jstiempos,
            "jsverbotipos" : jsverbotipos,
            "jspronombres" : jspronombres
            }

    return render(request,"verbos/palabras.html",context)


