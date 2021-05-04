from django.contrib import admin
from verbos.models import Conjugacion,Tiempo,Pronombre,Verbotipo,Verbo,Palabra,Palabratipo,Palabrafecha,Palabrafamilia,Palabragenero,Palabranivel

# Register your models here.
admin.site.register(Conjugacion)
admin.site.register(Tiempo)
admin.site.register(Verbo)
admin.site.register(Pronombre)
admin.site.register(Verbotipo)
admin.site.register(Palabra)
admin.site.register(Palabratipo)
admin.site.register(Palabrafecha)
admin.site.register(Palabrafamilia)
admin.site.register(Palabragenero)
admin.site.register(Palabranivel)




