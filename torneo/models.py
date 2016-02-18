from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q

# Create your models here.

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
    giocatore1 = models.CharField(max_length=200,verbose_name="Primo giocatore")
    giocatore2 = models.CharField(max_length=200,verbose_name="Secondo giocatore")
    punteggio = models.IntegerField(default=0)
    lunghezza = models.IntegerField(default=0)
    immagine = models.ImageField(upload_to='torneo/squadra',default='torneo/squadra/default.png')
    owner = models.ForeignKey(User,related_name="squadre",blank=True,default=None,null=True)
    confermata = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome + ' ('+ self.giocatore1 + ' - '+self.giocatore2 +')'

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
