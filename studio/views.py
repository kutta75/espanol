from django.shortcuts import render
import random,json,subprocess,datetime   
from django.forms.models import model_to_dict 



# Create your views here.
def index(request):
    title="studio" 
    cputemp1= "Server" 
    cputemp2= subprocess.getoutput("vcgencmd measure_temp")
    cputemp = cputemp1 + cputemp2 
    context= { 
            "title" : title,
            "cputemp": cputemp, 
            }
    return render(request,"studio/index.html",context)


