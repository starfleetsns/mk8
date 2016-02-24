from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.db.models import Q

# Create your models here.

class PreferenzeUtente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="preferenze")
    iscritto = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' iscritto: '+str(self.iscritto)

class DatiUtente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="dati")
    lunghezza = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' lungehzza: '+str(self.lunghezza)
    
    def ripunteggia(self):
        l = 0
        l += sum([ partita.punteggio11 for partite in [ squadra.partite1.filter(stato=Partita.DONE).all() for squadra in self.user.squadre1.all() ] for partita in partite ])
        l += sum([ partita.punteggio21 for partite in [ squadra.partite2.filter(stato=Partita.DONE).all() for squadra in self.user.squadre1.all() ] for partita in partite ])
        l += sum([ partita.punteggio12 for partite in [ squadra.partite1.filter(stato=Partita.DONE).all() for squadra in self.user.squadre2.all() ] for partita in partite ])
        l += sum([ partita.punteggio22 for partite in [ squadra.partite2.filter(stato=Partita.DONE).all() for squadra in self.user.squadre2.all() ] for partita in partite ])
        self.lunghezza = l
        self.save()
        return l

def funzione_scala(dl):
    if dl <= 0:
        return 0
    elif dl <= 10:
        return 1
    elif dl <= 30:
        return 2
    else:
        return 3

class Squadra(models.Model):
    nome = models.CharField(max_length=200,verbose_name="Nome della squadra")
    giocatore1 = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="Primo giocatore",related_name="squadre1")
    giocatore2 = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="Secondo giocatore",related_name="squadre2")
    punteggio = models.IntegerField(default=0)
    lunghezza = models.IntegerField(default=0)
    immagine = models.ImageField(upload_to='torneo/squadra',default='torneo/squadra/default.png')
    confermata = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome + ' ('+ str(self.giocatore1) + ' - '+ str(self.giocatore2) +')'

    def ripunteggia(self):
        p = 0
        p += sum([ funzione_scala(partita.dl()) for partita in self.partite1.filter(stato=Partita.DONE).all() ])
        p += sum([ funzione_scala(-partita.dl())for partita in self.partite2.filter(stato=Partita.DONE).all() ])
        l = 0
        l += sum([ partita.dl() for partita in self.partite1.filter(stato=Partita.DONE).all() ])
        l -= sum([ partita.dl() for partita in self.partite2.filter(stato=Partita.DONE).all() ])
        self.punteggio = p
        self.lunghezza = l
        self.save()
        return (p,l)
    
    def partite(self):
        return Partita.objects.filter(Q(squadra1=self)|Q(squadra2=self)).order_by('data').all()

    def giocatori(self):
        return [self.giocatore1, self.giocatore2]

class Partita(models.Model):    
    squadra1 = models.ForeignKey(Squadra,related_name="partite1",verbose_name="Prima squadra")
    squadra2 = models.ForeignKey(Squadra,related_name="partite2",verbose_name="Seconda squadra")
    punteggio11 = models.IntegerField(default=0,verbose_name="Prima squadra, primo giocatore")
    punteggio12 = models.IntegerField(default=0,verbose_name="Prima squadra, secondo giocatore")
    punteggio21 = models.IntegerField(default=0,verbose_name="Seconda squadra, primo giocatore")
    punteggio22 = models.IntegerField(default=0,verbose_name="Seconda squadra, secondo giocatore")

    INCOGNITA = "INC"
    ATTESA1 = "AT1"
    ATTESA2 = "AT2"
    DONE = "DON"

    stato = models.CharField(max_length=3,
                             choices=[ (INCOGNITA, "Partita non disputata" ),
                                       (ATTESA1, "In attesa di conferma dalla prima squadra"),
                                       (ATTESA2, "In attesa di conferma della seconda squadra"),
                                       (DONE, "Punteggio confermato"), ],
                             default = INCOGNITA)

    data = models.DateField()

    def __str__(self):
        return self.squadra1.nome + ' Vs ' +self.squadra2.nome + '  (' + str(self.data) + ')'

    def dl(self):
        return self.punteggio11 + self.punteggio12 - self.punteggio21 - self.punteggio22


#TODO: ForeingKey on_delete=RESTRICT
