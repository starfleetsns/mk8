from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q

# Create your models here.

class Squadra(models.Model):
    nome = models.CharField(max_length=200)
    giocatore1 = models.CharField(max_length=200)
    giocatore2 = models.CharField(max_length=200)
    punteggio = models.IntegerField(default=0)
    immagine = models.ImageField(upload_to='torneo/squadra',default='torneo/squadra/default.png')
    owner = models.ForeignKey(User,related_name="squadre",blank=True,default=None,null=True)
    confermata = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome + ' ('+ self.giocatore1 + ' - '+self.giocatore2 +')'

    def ripunteggia(self):
        p = 0
        p += sum([ partita.punteggio11 for partita in self.partite1.filter(stato=Partita.DONE).all() ])
        p += sum([ partita.punteggio12 for partita in self.partite1.filter(stato=Partita.DONE).all() ])
        p += sum([ partita.punteggio21 for partita in self.partite2.filter(stato=Partita.DONE).all() ])
        p += sum([ partita.punteggio22 for partita in self.partite2.filter(stato=Partita.DONE).all() ])
        self.punteggio = p
        self.save()
        return p
    
    def partite(self):
        return Partita.objects.filter(Q(squadra1=self)|Q(squadra2=self)).order_by('data').all()

class Partita(models.Model):    
    squadra1 = models.ForeignKey(Squadra,related_name="partite1")
    squadra2 = models.ForeignKey(Squadra,related_name="partite2")
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


#TODO: ForeingKey on_delete=RESTRICT
