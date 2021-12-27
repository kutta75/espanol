from django.shortcuts import render
from django import template 
from keyboard.models import Partition 
#from django import simplejson 
# Create your views here.


def index(request): 
    cadence = 2000
    partition=Partition.objects.first()
    portee_x = 300 
    portee_y = 180
    blackkey=[3.5,8.5,18.5,23.5,33.5,38.5,43.5,53.5,58.5,68.5,73.5,78.8,88.5,93.5,103.5,108.5]
    keysize=23
    blackkey=[3.5,8.5,13.5,23.5,28.5,38.5,43.5,48.5,58.5,63.5,73.5,78.8,83.5,93.5,98.5,108.5]
    if request.method=="POST":
        partition_selected=request.POST.getlist('partition')
        print("index - mode=post : " + partition_selected[0] )
        partition=Partition.objects.get(pk=partition_selected[0])
    partition_name=partition.name 
    partition_notes=partition.notes

    context = { 
            "cadence" : cadence ,
            "portee_x" : portee_x ,
            "portee_y" : portee_y ,
            "keytotal" : keysize ,
            "keysize" : range(keysize) ,
            "blackkey" : blackkey,
            "partition" : partition ,
            "partition_name" : partition_name ,
            "partition_note" : partition_notes ,
            }
    return render(request,"keyboard/index_portee.html",context) 

def partitions(request) : 
#    partitions=[["top1", [1,2,3,4,5,4,22,21,23,20,11,11,11]],["top2",[1,3,4,5,]]]
    partitions=Partition.objects.all()
    context = { 
            "partitions" : partitions ,
            } 
    return render(request,"keyboard/partitions.html",context) 
