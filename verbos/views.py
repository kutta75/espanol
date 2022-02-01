from django.shortcuts import render
import random,json,subprocess,datetime   
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
    title="Home" 
    cputemp1= "Server" 
    cputemp2= subprocess.getoutput("vcgencmd measure_temp")
    cputemp = cputemp1 + cputemp2 
    verbos = Verbo.objects.all()
    tiempos = Tiempo.objects.all()
    pronombres = Pronombre.objects.all()
    context= { 
            "title" : title,
            "cputemp": cputemp, 
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres
            }
    return render(request,"verbos/index.html",context)

def verbo(request,verbo_id):
    verbo= Verbo.objects.get(pk=verbo_id)
    context = { 
            "verbo" : verbo ,
            "title" : "Verbo" , 
            "conjugacions" : verbo.conjugacions.all().order_by('tiempo__tiemposeq')
            }
    return render(request,"verbos/verbo.html",context)

def gramatica(request):
    title="Gramatica" 
    context = { 
            "title" : title ,
            }
    return render(request,"verbos/gramatica.html",context)

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
            "title" : "verbos liste" , 
            "tiempos" : tiempos , 
            "pronombres" : pronombres
            }
    return render(request,"verbos/verbos.html",context)




def verbos_exo(request,mode_id,conjugacion_id):
    resuelto = " sabes tus conjugaciones ? "
    trace= "<= puedes utilizar estas lettras"
    tracerep= "  "
    trace_id= "  "
    # cas du premier appel à cette page ; initialisation des parametres et proposition d'une conjugaison aléatoirement parmi 
    # toutes celles disponibles 
    if request.method=="GET":
        Conjugacion_selectadas_count = Conjugacion.objects.count() 
        loto_winner=random.randint(0,Conjugacion_selectadas_count-1)
        # ici on cherche à retrouver l'index du verbe gagnant dans le queryset  Verbos complet 
        Conjugacion_selectadas_list=Conjugacion.objects.values_list('pk',flat=True)
        Conjugacion_winner_pk=Conjugacion_selectadas_list[loto_winner]
        print("loto winner = " + str(loto_winner))
        Conjugacion_winner=Conjugacion.objects.get(pk=Conjugacion_winner_pk)
        
    if request.method=="POST":
        if mode_id==1:
    # traitement de la reponse apportée i a la question rang n-1 en comparant avec la question posée 
    # rang n-1 dont on connait l'idi du verbe qui a servi à la question 
            respuesta= request.POST.getlist('respuesta')
            conjugacion = Conjugacion.objects.get(pk=conjugacion_id)
            # preparation du texte à afficher pour présenter la bonne reponse 
            trace = str(conjugacion.verbo) + " " + str(conjugacion.tiempo) + " " + str(conjugacion.pronombre) +" => " + str(conjugacion.conjugacion)   
            tracerep =  str(respuesta[0]) 
            trace_id =  str(conjugacion.id) 
            # nettoyage des espaces qui pourraient etre dans les 2 chaines 
            if respuesta[0].replace(" ","").lower() == conjugacion.conjugacion.replace(" ",""):
                resuelto="1"
            else:
                resuelto="0"

# preparation de la question suivante en exploitant les criteres de selection pour trouver une nouvelle conjugaion aleatoirement 
# recuperation des filtres selectionnés 
        verbotipos_selected= request.POST.getlist('verbotipo')
        pronombres_selected= request.POST.getlist('pronombre')
        tiempos_selected= request.POST.getlist('tiempo')
        levels_selected= request.POST.getlist('level')
        # construction du queryset basé sur la selections des checkbox 
        
        Conjugacion_selectadas=Conjugacion.objects.filter(tiempo__in=tiempos_selected).filter(pronombre__in=pronombres_selected).filter(verbo__in=Verbo.objects.filter(tipo__in=verbotipos_selected)).filter(level__in=levels_selected)
        # comptage du nombre d'objets selectionnés  
        Conjugacion_selectadas_count =Conjugacion_selectadas.count()
        # si le nombre est supérieur 1 alors on choix d'un objet aléatoirement dans cette liste       
        if Conjugacion_selectadas_count  > 0 :
            loto_winner=random.randint(0,Conjugacion_selectadas_count-1)
            print("loto winner = " + str(loto_winner))
            # ici on cherche à retrouver l'index du verbe gagnant dans le queryset  Verbos complet 
            Conjugacion_selectadas_list=Conjugacion_selectadas.values_list('pk',flat=True)
            Conjugacion_winner_pk=Conjugacion_selectadas_list[loto_winner]
            print("Conjugacion  selectada  pk =" + str(Conjugacion_winner_pk))
            Conjugacion_winner=Conjugacion.objects.get(pk=Conjugacion_winner_pk) 
        else:
            # cas  ou le filtre apporte 0 reccord :  on blucle sur le précédent item ..  
            #respuesta= request.POST.getlist('respuesta')
        #conjugacion = Conjugacion.objects.get(pk=conjugacion_id)
         #   Conjugacion_selectadas_count = Conjugacion.objects.count() 
        #    loto_winner=random.randint(0,Conjugacion_selectadas_count-1)
            # ici on cherche à retrouver l'index du verbe gagnant dans le queryset  Verbos complet 
         #   Conjugacion_selectadas_list=Conjugacion.objects.values_list('pk',flat=True)
          #  Conjugacion_winner_pk=Conjugacion_selectadas_list[loto_winner]
          #  print("loto winner = " + str(loto_winner))
            pk_winner=conjugacion_id
            Conjugacion_winner_pk=conjugacion_id
            loto_winner=-1  
            Conjugacion_winner=Conjugacion.objects.get(pk=conjugacion_id)
            Conjugacion_selectadas_count = 0 # pour transmettre dans le template 
            
        
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

    # myset set à porter la liste des objets qui servent à faire des  filtres pour les exo 
    myset=("tiempos","pronombres","verbotipos")

    jstiempos=jslist(tiempos)
    jspronombres=jslist(pronombres)
    jsverbotipos=jslist(verbotipos)
    jslevels=jslist(levels)
    context= { 
            "title" : "Verbos exo", 
            "verbos" : verbos,
            "tiempos" : tiempos , 
            "pronombres" : pronombres,
            "levels" : levels,
            "verbotipos" : verbotipos,
            "tiempos_checked": tiempos_checked,
            "verbotipos_checked": verbotipos_checked,
            "pronombres_checked": pronombres_checked,
            "conjugacion_selectada" : Conjugacion_winner,
            "conjugacion_selectada_count" : Conjugacion_selectadas_count,
            "loto_winner" : loto_winner,
            "pk_winner" : Conjugacion_winner_pk,
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

def vocabulario(request,mode_id,palabra_id):
    # exercice de vocabulaire : proposition d'un mot à traduire  : le mot est sélectionné en de listes de choix à cliquer préalablement 
    # fonction d'affichages de domaines / type  / niveau / date des palabra
    # instanciation initiale de la liste familia_checked qui supportera la selection des cases à cocher des termes
    # selectionnés par l'utilisateur 
    familias_selected=[]
    familias_txt=[]
    Palabra_winner=Palabra.objects.first()
    Palabra_winner_prev = Palabra.objects.first()
    Palabra_selectada_count= 0
    print("type du first element")
    Palabra_selectadas=Palabra.objects.all() 

    familias  = Palabrafamilia.objects.all()
    tipos  =    Palabratipo.objects.all()
    generos =   Palabragenero.objects.all()
    nivels =    Palabranivel.objects.all() 
    fechas =    Palabrafecha.objects.all().order_by('palabrafecha') 
    
    # cas de l'arrivée initiale dans l'ecran 
    if mode_id ==0 : 
        mode = "start"

    if mode_id ==1 : 
        mode = "run"
    if request.method=="GET":
        Palabra_selectadas=Palabra.objects.all() 
    # request post 
    # ici c'est un retour depuis un test deja soumis : la tache ici est de recuperer la réponse correspondant à l'idi palabra_id
    # pour afficher tous les champs de réponse  
    if request.method=="POST":
        # recuperation du test precedent pour afficher la reponse 
        if mode_id==1:
            Palabra_winner_prev = Palabra.objects.get(pk=palabra_id)
        # recuperation de la liste familia_post qui contient les "value" des box qui ont été selectionées
        familias_selected = request.POST.getlist('familia')
        tipos_selected = request.POST.getlist('tipo')
        fechas_selected = request.POST.getlist('fecha')
        nivels_selected = request.POST.getlist('nivel')
        # construction du queryset basé sur la selections des checkbox 
        Palabra_selectadas =Palabra.objects.filter(palabrafamilia__in=familias_selected).filter(palabratipo__in=tipos_selected).filter(palabrafecha__in=fechas_selected).filter(palabranivel__in=nivels_selected)
        # contage du nombre d'element du queryset  
        Palabra_selectada_count =Palabra_selectadas.count()
        #    familias_txt = familias_txt + str(familias_selected[i]) 
        if Palabra_selectada_count > 0 :
            loto_winner=random.randint(0,Palabra_selectada_count-1)
            print("loto winner = " + str(loto_winner))
            Palabra_selectada_list=Palabra_selectadas.values_list('pk',flat=True)
            Palabra_winner_pk=Palabra_selectada_list[loto_winner]
            print("Palabra selecta pk =" + str(Palabra_winner_pk))
            Palabra_winner=Palabra.objects.get(pk=Palabra_winner_pk)
                    
    print("palabra_winner.id"  ) 
    

    # myset sert à porter la liste des objets qui servent à faire des  filtres pour les exo 
    jsfamilias=jslist(familias)
    jstipos =jslist(tipos)
    jsgeneros=jslist(generos)
    jsnivels=jslist(nivels)
    jsfechas=jslist(fechas)
    context= {
            "title" : "Vocabulario" , 
            "mode" : mode , 
            "familias" : familias,
            "jsfamilias" : jsfamilias,
            "familias_selected" : familias_selected,
            "familias_txt" : familias_txt, 
            "tipos" : tipos,
            "jstipos" : jstipos , 
            "generos" : generos,
            "jsgeneros" : jsgeneros , 
            "nivels" : nivels , 
            "jsnivels" : jsnivels ,
            "fechas" : fechas,
            "jsfechas" : jsfechas ,
            "Palabra_winner" : Palabra_winner,
            "Palabra_winner_prev" : Palabra_winner_prev,
            "Palabra_selectada_count" : Palabra_selectada_count , 
            "Palabra_selectadas" : Palabra_selectadas , 
        }

    return render(request,"verbos/vocabulario.html",context)

def anuncios_clasificados(request):
    titre="Conversaciones francés - español"
    texto="Francés aprendiendo español propone conversaciones mitad en francés / mitad en español a alguno/a que tiene español como lengua materna (para mejorar el nivel de los dos alumnos…). Propongo hacerlo una vez cada semana, durante hasta una hora ( Vivo en Paris 19ieme y soy un hombre adulto ). " 
    mail = "kutta75@gmail.com" 
    fecha = "01/07/2021"
    context= { 
            "titre" : titre ,
            "texto" : texto ,
            "fecha" : fecha, 
            "mail" : mail ,
            }

    return render(request,"verbos/anuncios_clasificados.html",context)

