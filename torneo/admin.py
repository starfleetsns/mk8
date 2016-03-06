from django.contrib import admin
from torneo.models import Squadra,Partita,PreferenzeUtente,DatiUtente
from django.contrib.auth.models import User

from django.contrib import messages

# Register your models here.

class PartitaAdmin(admin.ModelAdmin):
    fields = ['data','squadra1','squadra2','punteggio11','punteggio12','punteggio21','punteggio22','stato','campionato','gare']
    list_display = ['data','squadra1','squadra2', 'stato','campionato','gare']
    list_filter = ['data','stato','campionato']

    
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        instance.squadra1.ripunteggia()
        instance.squadra2.ripunteggia()
        for user in [ instance.squadra1.giocatore1 , instance.squadra1.giocatore2, instance.squadra2.giocatore1, instance.squadra2.giocatore2 ]:
            dati, created = DatiUtente.objects.get_or_create(user=user)
            dati.ripunteggia()
        # for squadra in Squadra.objects.all():
        #     squadra.ripunteggia()
        return instance

   
class SquadraAdmin(admin.ModelAdmin):
    list_display = ['nome','giocatore1','giocatore2','confermata']
    list_filter = ['confermata']

    def conferma(self, request, queryset):
        queryset.update(confermata=True)
    conferma.short_description = "Conferma le squadre selezionate"

    actions = [conferma]

class PreferenzeUtenteAdmin(admin.ModelAdmin):
    list_filter = ['iscritto']
    
admin.site.register(Squadra, SquadraAdmin)
admin.site.register(Partita, PartitaAdmin)
admin.site.register(PreferenzeUtente, PreferenzeUtenteAdmin)

