from django.shortcuts import render
import random,json,subprocess,datetime,re   
from django.forms.models import model_to_dict 
from verbos.models import Verbo,Tiempo,Conjugacion,Pronombre,Verbotipo,Level,Palabra,Palabratipo,Palabragenero,Palabranivel,Palabrafamilia,Palabrafecha,Sub_modelo,Sub_princ,Sub_conj


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
    
    # init de la liste des idi des conjugaison en erreur
    conjugacion_error_list=[] 
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
        # mode_id = 1 
        
    if request.method=="POST":
        if mode_id==1:
    # traitement de la reponse apportée i a la question rang n-1 en comparant avec la question posée 
    # rang n-1 dont on connait l'idi du verbe qui a servi à la question 
            respuesta= request.POST.getlist('respuesta')
            conjugacion = Conjugacion.objects.get(pk=conjugacion_id)
            # preparation du texte à afficher pour présenter la bonne reponse 
            trace = str(conjugacion.verbo) + " " + str(conjugacion.tiempo) + " " + str(conjugacion.pronombre) +" = " + str(conjugacion.conjugacion)   
            tracerep =  str(respuesta[0]) 
            trace_id =  str(conjugacion.id) 
            # nettoyage des espaces qui pourraient etre dans les 2 chaines 
            if respuesta[0].replace(" ","").lower() == conjugacion.conjugacion.replace(" ",""):
                resuelto="1"
            else:
                resuelto="0"
                conjugacion_error_list.append(conjugacion_id)
       # recuperation des filtres selectionnés 
        verbotipos_selected= request.POST.getlist('verbotipo')
        pronombres_selected= request.POST.getlist('pronombre')
        tiempos_selected= request.POST.getlist('tiempo')
        levels_selected= request.POST.getlist('level')
        # recuperation de la variable play_mode 
        play_mode=request.POST.getlist('play_mode_name')
        print(" play_mode_name = "+ str(play_mode)) 
        if not (play_mode):
            print("mode run")
            # ici on travaille en cherchant une nouvelle conjugaison prise au hasard en fonction des filtres posées 
            # preparation de la question suivante en exploitant les criteres de selection pour trouver une nouvelle conjugaion aleatoirement 
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
        else:
            print("mode error "+ str(play_mode))
            conjugacion_error_list_id=play_mode[0].split(',')
            print("conjugacion error list id = " + str(conjugacion_error_list_id ))
            loto_winner=random.randint(1,len(conjugacion_error_list_id)-1)
            Conjugacion_winner_pk=int(conjugacion_error_list_id[loto_winner])
            print("mode error : loto winner =" + str(loto_winner) + " pk winner =" + str(Conjugacion_winner_pk) ) 
            Conjugacion_winner=Conjugacion.objects.get(pk=Conjugacion_winner_pk) 
            Conjugacion_selectadas_count =len(conjugacion_error_list_id)-1



# preparation de la question suivante en exploitant les criteres de selection pour trouver une nouvelle conjugaion aleatoirement 
# recuperation des filtres selectionnés 
 #       verbotipos_selected= request.POST.getlist('verbotipo')
 #       pronombres_selected= request.POST.getlist('pronombre')
 #       tiempos_selected= request.POST.getlist('tiempo')
 #       levels_selected= request.POST.getlist('level')
        # construction du queryset basé sur la selections des checkbox 
        
 #       Conjugacion_selectadas=Conjugacion.objects.filter(tiempo__in=tiempos_selected).filter(pronombre__in=pronombres_selected).filter(verbo__in=Verbo.objects.filter(tipo__in=verbotipos_selected)).filter(level__in=levels_selected)
        # comptage du nombre d'objets selectionnés  
 #       Conjugacion_selectadas_count =Conjugacion_selectadas.count()
        # si le nombre est supérieur 1 alors on choix d'un objet aléatoirement dans cette liste       
 #       if Conjugacion_selectadas_count  > 0 :
 #           loto_winner=random.randint(0,Conjugacion_selectadas_count-1)
 #           print("loto winner = " + str(loto_winner))
 #           # ici on cherche à retrouver l'index du verbe gagnant dans le queryset  Verbos complet 
 #           Conjugacion_selectadas_list=Conjugacion_selectadas.values_list('pk',flat=True)
 #           Conjugacion_winner_pk=Conjugacion_selectadas_list[loto_winner]
 #           print("Conjugacion  selectada  pk =" + str(Conjugacion_winner_pk))
 #           Conjugacion_winner=Conjugacion.objects.get(pk=Conjugacion_winner_pk) 
 #       else:
            # cas  ou le filtre apporte 0 reccord :  on blucle sur le précédent item ..  
            #respuesta= request.POST.getlist('respuesta')
        #conjugacion = Conjugacion.objects.get(pk=conjugacion_id)
         #   Conjugacion_selectadas_count = Conjugacion.objects.count() 
        #    loto_winner=random.randint(0,Conjugacion_selectadas_count-1)
            # ici on cherche à retrouver l'index du verbe gagnant dans le queryset  Verbos complet 
         #   Conjugacion_selectadas_list=Conjugacion.objects.values_list('pk',flat=True)
          #  Conjugacion_winner_pk=Conjugacion_selectadas_list[loto_winner]
          #  print("loto winner = " + str(loto_winner))
 #           pk_winner=conjugacion_id
 #           Conjugacion_winner_pk=conjugacion_id
 #           loto_winner=-1  
 #           Conjugacion_winner=Conjugacion.objects.get(pk=conjugacion_id)
 #           Conjugacion_selectadas_count = 0 # pour transmettre dans le template 
            
        
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
            "conjugacion_error_list" : conjugacion_error_list,
            "loto_winner" : loto_winner,
            "pk_winner" : Conjugacion_winner_pk,
            "resuelto" : resuelto,
            "trace" : trace,
            "trace_id" : trace_id,
            "mode_id" : mode_id,
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
    fechas =    Palabrafecha.objects.all().order_by('-palabrafecha') 
    lose_excluded=[]

    # cas de l'arrivée initiale dans l'ecran 
    if mode_id ==0 : 
        mode = "start"

    if mode_id ==1 : 
        mode = "run"
    if request.method=="GET":
        Palabra_selectadas=Palabra.objects.all() 
        Palabra_selectada_count= Palabra_selectadas.count() 
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
        generos_selected = request.POST.getlist('genero')
        # instanciation de  la liste des noms à exclure
        # la liste se presente comme une chaine de car dans le premier element de la liste lose_list
        # ( qui vient d'un bouton invisible html)
        # on doit donc d'abord recuperer cette chaine / la splitter dans une liste 
        lose_excluded_str = re.split(',',request.POST.getlist('lose_list')[0] )
        # et pour chaque element de la liste on doit el convertir  en entier 
        lose_excluded=list(map(lambda x: int(x),lose_excluded_str))
        #print("-> lose_excluded="+str(lose_excluded),type(lose_excluded),str(len(lose_excluded)))
        #print("-> lose_excluded="+str(lose_excluded),type(lose_excluded),str(len(lose_excluded)))
        # construction du queryset basé sur la selections des checkbox 
        #print("-> lose_excluded="+str(lose_excluded),type(lose_excluded),str(len(lose_excluded)))
#        Palabra_selectadas_all =Palabra.objects.filter(palabrafamilia__in=familias_selected).filter(palabratipo__in=tipos_selected).filter(palabrafecha__in=fechas_selected).filter(palabranivel__in=nivels_selected).filter(palabragenero__in=generos_selected)
#        Palabra_selectadas =Palabra_selectadas_all.exclude(id__in=lose_excluded)
        Palabra_selectadas =Palabra.objects.filter(palabrafamilia__in=familias_selected).filter(palabratipo__in=tipos_selected).filter(palabrafecha__in=fechas_selected).filter(palabranivel__in=nivels_selected).filter(palabragenero__in=generos_selected).exclude(id__in=lose_excluded)
        # comptage du nombre d'element du queryset  
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
            "lose_excluded" : lose_excluded ,
            "mode_id" : mode_id , 
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

def subjuntivo(request,id1,id2):
    titre="Conversaciones francés - español"
    texto="Francés aprendiendo español propone conversaciones mitad en francés / mitad en español a alguno/a que tiene español como lengua materna (para mejorar el nivel de los dos alumnos…). Propongo hacerlo una vez cada semana, durante hasta una hora ( Vivo en Paris 19ieme y soy un hombre adulto ). " 
    mail = "kutta75@gmail.com" 
    fecha = "01/07/2021"
    # traitement d'un retour apres saisie d une selection / proposition de reponse
    if request.method =="GET":
        princ="Estas listo ?"
        conjugacion=" prueba !"
        conj=" cual es la conjugacion ? "
    if request.method =="POST":
        modelos_selected=request.POST.getlist('modelo')
        respuesta=request.POST.getlist('resel 10puesta')
        # selection d'un modele parmi ceux selectionné dans les cases à coché
        Princ_selectadas = Sub_princ.objects.filter(sub_modelo__in=modelos_selected)
        # contage du nombre d'element du queryset  
        Princ_selectadas_count =Princ_selectadas.count()
        #    familias_txt = familias_txt + str(familias_selected[i]) 
        if Princ_selectadas_count > 0 :
            loto_winner=random.randint(0,Princ_selectadas_count-1)
            print("loto winner = " + str(loto_winner))
            Princ_selectada_list=Princ_selectadas.values_list('pk',flat=True)
            Princ_winner_pk=Princ_selectada_list[loto_winner]
            print("Princ selecta pk =" + str(Princ_winner_pk))
            Princ_winner=Sub_princ.objects.get(pk=Princ_winner_pk)
            princ=Princ_winner
        # selection d'une conjunction associée à ce modele 
        print(" modelo selection " + str(Princ_winner.sub_modelo))
        Conj_selectadas = Sub_conj.objects.filter(sub_conj_modelo=Princ_winner.sub_modelo)
        # contage du nombre d'element du queryset  
        Conj_selectadas_count =Conj_selectadas.count()
        #    familias_txt = familias_txt + str(familias_selected[i]) 
        if Conj_selectadas_count > 0 :
            loto_winner=random.randint(0,Conj_selectadas_count-1)
            print("loto winner = " + str(loto_winner))
            Conj_selectada_list=Conj_selectadas.values_list('pk',flat=True)
            Conj_winner_pk=Conj_selectada_list[loto_winner]
            print("Conj selecta pk =" + str(Conj_winner_pk))
            Conj_winner=Sub_conj.objects.get(pk=Conj_winner_pk)
            conj=Conj_winner
        # selection d'une conjugaison pour la subordonnée dans un temps adapté à la principale
        Tiempo_selected=Tiempo.objects.filter(tiemposeq=Princ_winner.sub_tiempo_seq)
        Conjugacion_selectadas=Conjugacion.objects.filter(tiempo__in=Tiempo_selected)
        Conjugacion_selectadas_count =Conjugacion_selectadas.count()
        #    familias_txt = familias_txt + str(familias_selected[i]) 
        if Conjugacion_selectadas_count > 0 :
            loto_winner=random.randint(0,Conjugacion_selectadas_count-1)
            print("loto winner = " + str(loto_winner))
            Conjugacion_selectadas_list=Conjugacion_selectadas.values_list('pk',flat=True)
            Conjugacion_winner_pk=Conjugacion_selectadas_list[loto_winner]
            print("Conjuga selecta pk =" + str(Conjugacion_winner_pk))
            Conjugacion_winner=Conjugacion.objects.get(pk=Conjugacion_winner_pk)
            conjugacion=Conjugacion_winner


    modelos=Sub_modelo.objects.all()
    jsmodelos=jslist(modelos) 
    context= { 
            "titre" : titre ,
            "texto" : texto ,
            "fecha" : fecha, 
            "mail" : mail ,
            "conj" : conj ,
            "princ" : princ,
            "jsmodelos" : jsmodelos ,
            "modelos" : modelos,
            "conjugacion" : conjugacion
            }

    return render(request,"verbos/subjuntivo.html",context)
