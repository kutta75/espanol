"""espanol URL Configuration
Dom maj 9/3/2021 

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView 
from verbos import views
from django.contrib.staticfiles.storage import staticfiles_storage 

urlpatterns = [
    path("", views.index,name='index'),
    path('<int:verbo_id>',views.verbo,name='verbo'),
    path('verbos/',views.verbos,name='verbos'),
    path('verbos_exo/<int:mode_id>/<int:conjugacion_id>',views.verbos_exo,name='verbos_exo_run'),
    path('verbos_exo/',views.verbos_exo,name='verbos_exo'),
    path('palabras/<int:id1>/<int:id2>',views.palabras,name='palabras'),
    path('palabra/',views.palabra,name='palabra'),
    path('vocabulario/<int:mode_id>/<int:palabra_id>',views.vocabulario,name='vocabulario_run'),
    path('vocabulario/',views.vocabulario,name='vocabulario'),
    path('favico.ico',RedirectView.as_view(url=staticfiles_storage.url('img/favico.ico')))
        ]
