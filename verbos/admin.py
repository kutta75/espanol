from django.contrib import admin
from verbos.models import Conjugacion,Tiempo,Pronombre,Verbotipo,Verbo

# Register your models here.
admin.site.register(Conjugacion)
admin.site.register(Tiempo)
admin.site.register(Verbo)
admin.site.register(Pronombre)
admin.site.register(Verbotipo)

