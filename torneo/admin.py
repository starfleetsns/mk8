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

   
class SquadraAdmin(admin.ModelAdmin):
    list_display = ['nome','owner','giocatore1','giocatore2','confermata']
    list_filter = ['confermata']

    def conferma(self, request, queryset):
        queryset.update(confermata=True)
    conferma.short_description = "Conferma le squadre selezionate"

    actions = [conferma]

admin.site.register(Squadra, SquadraAdmin)
admin.site.register(Partita, PartitaAdmin)

