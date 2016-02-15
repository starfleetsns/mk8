from django.contrib import admin
from torneo.models import Squadra,Partita

# Register your models here.

class PartitaAdmin(admin.ModelAdmin):
    #fields = ['data','squadra1','squadra2','punteggio1','punteggio2']
    list_display = ['data','squadra1','squadra2','punteggio1','punteggio2', 'done']
    list_filter = ['data','done']

    
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if (instance.punteggio1 > 0) and (instance.punteggio2 > 0):
            instance.done = True
        instance.save()
        # instance.squadra1.ripunteggia()
        # instance.squadra2.ripunteggia()        
        # instance.squadra1.save()
        # instance.squadra2.save()
        for squadra in Squadra.objects.all():
            squadra.ripunteggia()
        form.save_m2m()
        return instance
        

admin.site.register(Squadra)
admin.site.register(Partita, PartitaAdmin)

