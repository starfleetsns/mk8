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
        p += sum([ partita.punteggio1 for partita in self.partite1.all() ])
        p += sum([ partita.punteggio2 for partita in self.partite2.all() ])
        self.punteggio = p
        self.save()
        return p
    
    def partite(self):
        return Partita.objects.filter(Q(squadra1=self)|Q(squadra2=self)).order_by('data').all()

class Partita(models.Model):    
    squadra1 = models.ForeignKey(Squadra,related_name="partite1")
    squadra2 = models.ForeignKey(Squadra,related_name="partite2")
    punteggio1 = models.IntegerField(default=0)
    punteggio2 = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
    data = models.DateField()

    def __str__(self):
        return self.squadra1.nome + ' Vs ' +self.squadra2.nome + '  (' + str(self.data) + ')'


#TODO: ForeingKey on_delete=RESTRICT
