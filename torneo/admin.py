from django.contrib import admin
from torneo.models import Squadra,Partita

from django.contrib import messages

# Register your models here.

class PartitaAdmin(admin.ModelAdmin):
    fields = ['data','squadra1','squadra2','punteggio1','punteggio2']
    list_display = ['data','squadra1','squadra2','punteggio1','punteggio2', 'done']
    list_filter = ['data','done']

    
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if (instance.punteggio1 > 0) and (instance.punteggio2 > 0):
            instance.done = True
        elif (instance.punteggio1 == 0) and (instance.punteggio2 == 0):
            instance.done = False
        else:
            messages.error(request, 'Non capisco se sia stata disputata la partita o no, quindi non salvo!')
            return instance
        instance.save()
        form.save_m2m()
        # instance.squadra1.ripunteggia()
        # instance.squadra2.ripunteggia()        
        # instance.squadra1.save()
        # instance.squadra2.save()
        for squadra in Squadra.objects.all():
            squadra.ripunteggia()
        return instance
        

admin.site.register(Squadra)
admin.site.register(Partita, PartitaAdmin)

