from django.contrib import admin
from verbos.models import Conjugacion,Tiempo,Pronombre,Verbotipo,Verbo,Palabra,Palabratipo,Palabrafecha,Palabrafamilia,Palabragenero,Palabranivel
from verbos.models import Sub_modelo,Sub_conj,Sub_princ

# Register your models here.
class TiempoAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'tiempo','tiemposeq' ]
class PronombreAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'pronombre','pronombreseq' ]
class Sub_conjAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'sub_conj' ]
class Sub_conjAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'sub_conj' ]

class Sub_princAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'sub_princ' ]

class Sub_princAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'sub_princ', 'sub_modelo']
admin.site.register(Conjugacion)
admin.site.register(Tiempo,TiempoAdmin)
admin.site.register(Verbo)
admin.site.register(Pronombre,PronombreAdmin)
admin.site.register(Verbotipo)
admin.site.register(Palabra)
admin.site.register(Palabratipo)
admin.site.register(Palabrafecha)
admin.site.register(Palabrafamilia)
admin.site.register(Palabragenero)
admin.site.register(Palabranivel)
admin.site.register(Sub_modelo,Sub_princAdmin)
admin.site.register(Sub_conj,Sub_conjAdmin)
admin.site.register(Sub_princ,Sub_princAdmin)




