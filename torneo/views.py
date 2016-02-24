from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.views.generic.edit import CreateView,UpdateView,DeleteView,ModelFormMixin
from django.views.generic import ListView
from torneo.models import Squadra,Partita,PreferenzeUtente,DatiUtente
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
#from django.forms import ModelForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here.

def squadreid(request,idsquadra):
    squadra = get_object_or_404(Squadra,pk=idsquadra)
    partite = squadra.partite()
    return render(request,'torneo/squadreid.html',{'squadra':squadra,'partite':partite})

def classifica(request):
    squadre = Squadra.objects.filter(confermata=True).order_by('-punteggio','-lunghezza').all()
#    lista = [ {'pos':i+1 , 's':squadre[i] } for i in range(len(squadre))]
    return render(request,'torneo/classifica.html',{'lista':squadre})

#def squadre(request):
#    lista = Squadra.objects.order_by('nome').all()
#    return render(request,'torneo/squadre.html',{'lista':lista})

def calendario(request):
    lista = Partita.objects.order_by('data')
    return render(request,'torneo/calendario.html',{'lista':lista})

#def default(request):
#    return redirect('torneo:regolamento')

def signage(request):
    squadre = Squadra.objects.filter(confermata=True).order_by('-punteggio','-lunghezza').all()[:3]
    giocatori = User.objects.filter(preferenze__iscritto=True).order_by('-dati__lunghezza').all()[:3]
    return render(request,'torneo/signage.html',{'squadre':squadre,'giocatori':giocatori})

def index(request):
    context = {
        'nsquadre': Squadra.objects.filter(confermata=True).count(),
        'npartite':  Partita.objects.count(),
        'npartitedone' : Partita.objects.filter(stato=Partita.DONE).count(),
        'ngiocatori': User.objects.filter(preferenze__iscritto=True).count(),
        'authenticated' : request.user.is_authenticated(),
        }
    if ('splash' not in request.session):
        request.session['splash'] = False
        context['animazione'] = True
    else:
        context['animazione'] = False

    return render(request,'torneo/index.html',context)

def regolamento(request):
    return render(request,'torneo/regolamento.html')

class SquadreNuova(CreateView):
    model = Squadra
    fields = ['nome','giocatore2','immagine']
    
    success_url = '/torneo/squadre/'

    def get_form(self,form_class):
        form = super(SquadreNuova,self).get_form(form_class)
        form.fields['giocatore2'].queryset = User.objects.filter(preferenze__iscritto=True).exclude(pk=self.request.user.pk)
        return form
    
#    @method_decorator(login_required)
    def form_valid(self,form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        if not hasattr(self.request.user,'preferenze'):
            raise PermissionDenied
        if not self.request.user.preferenze.iscritto:
            raise PermissionDenied
        form.instance.giocatore1 = self.request.user
        return super(SquadreNuova, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not hasattr(self.request.user,'preferenze'):
            return redirect('torneo:giocatoripreferenze')
        if not self.request.user.preferenze.iscritto:
            return redirect('torneo:giocatoripreferenze')
        return super(SquadreNuova, self).dispatch(*args, **kwargs)
    

class SquadreModifica(UpdateView):
    model = Squadra
    fields = ['immagine']
    
    def get_object(self):
        squadra = super(SquadreModifica, self).get_object()
        if self.request.user.is_superuser or self.request.user.has_perm('torneo.change_squadra'):
            return squadra
        else:
            if self.request.user in squadra.giocatori():
                return squadra
            else:
                raise PermissionDenied
            
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SquadreModifica, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('torneo:squadreid',kwargs={'idsquadra':self.get_object().id})

class SquadreCancella(DeleteView):
    model = Squadra
    
    def get_object(self):
        squadra = super(SquadreCancella, self).get_object()
        if self.request.user.is_superuser or self.request.user.has_perm('torneo.delete_squadra'):
            return squadra
        else:
            raise PermissionDenied
#            if self.request.user in squadra.giocatori():
#                return squadra
#            else:
#                raise PermissionDenied
            
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SquadreCancella, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('torneo:squadre')

class SquadreLista(ListView):
    model = Squadra
    mie = False

    def get_queryset(self):
        base_qs = super(SquadreLista,self).get_queryset()
        qs = base_qs.order_by('-confermata','nome')
        if self.mie:
            return qs.filter(Q(giocatore1=self.request.user)|Q(giocatore2=self.request.user))
        else:
            return qs


class PartiteModifica(UpdateView):
    model = Partita
    fields = ['data','punteggio11','punteggio12','punteggio21','punteggio22']
#    form_class =  modelform_factory(Kunde, widgets={"data": SelectDateWidget })
    
    
    def get_object(self):
        partita = super(PartiteModifica, self).get_object()
        if partita.stato != Partita.INCOGNITA:
            if (self.request.user in partita.squadra1.giocatori()) and (partita.stato == Partita.ATTESA2):
                return partita
            elif (self.request.user in partita.squadra2.giocatori()) and (partita.stato == Partita.ATTESA1):
                return partita
            else:
                raise PermissionDenied
        if (self.request.user in partita.squadra1.giocatori()) or (self.request.user in partita.squadra2.giocatori()):
            return partita
        else:
            raise PermissionDenied
            
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PartiteModifica, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('torneo:partitemie')

    def form_valid(self,form):
        if self.request.user in form.instance.squadra1.giocatori():
            if self.request.user in form.instance.squadra2.giocatori():
                form.instance.stato=Partita.DONE
                form.instance.save()
                instance.squadra1.ripunteggia()
                instance.squadra2.ripunteggia()
                for user in [ instance.squadra1.giocatore1 , instance.squadra1.giocatore2, instance.squadra2.giocatore1, instance.squadra2.giocatore2 ]:
                    dati, created = DatiUtente.objects.get_or_create(user=user)
                    dati.ripunteggia()
                # for squadra in Squadra.objects.all():
                #     squadra.ripunteggia()
            else:
                form.instance.stato=Partita.ATTESA2
        elif self.request.user in form.instance.squadra2.giocatori():
            form.instance.stato=Partita.ATTESA1
        else:
            raise PermissionDenied
        return super(PartiteModifica,self).form_valid(form)

class PartiteApprova(UpdateView):
    model = Partita
    fields = []
    template_name = 'torneo/partite_approva.html'
    
    def get_object(self):
        partita = super(PartiteApprova, self).get_object()
        if (self.request.user in partita.squadra1.giocatori()) and (partita.stato == Partita.ATTESA1):
            return partita
        elif (self.request.user in partita.squadra2.giocatori()) and (partita.stato == Partita.ATTESA2):
            return partita
        else:
            raise PermissionDenied

    def get_context_data(self, *args, **kwargs):
        context = super(PartiteApprova, self).get_context_data(*args, **kwargs)
        context['azione'] = self.kwargs['azione']
        context['partita'] = self.get_object()
        return context
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PartiteApprova, self).dispatch(*args, **kwargs)

    def form_valid(self,form):
        if self.kwargs['azione'] == 'approva':
            form.instance.stato = Partita.DONE
            form.instance.save()
            form.instance.squadra1.ripunteggia()
            form.instance.squadra2.ripunteggia()
            for user in [ form.instance.squadra1.giocatore1 , form.instance.squadra1.giocatore2, form.instance.squadra2.giocatore1, form.instance.squadra2.giocatore2 ]:
                dati, created = DatiUtente.objects.get_or_create(user=user)
                dati.ripunteggia()
            # for squadra in Squadra.objects.all():
            #     squadra.ripunteggia()
        elif self.kwargs['azione'] == 'rifiuta':
            form.instance.stato = Partita.INCOGNITA
        else:
            raise PermissionDenied
        return super(PartiteApprova,self).form_valid(form)

    def get_success_url(self):
        return reverse('torneo:partitemie')

class PartiteLista(ListView):
    model = Partita
    mie = False

    def get_queryset(self):
        base_qs = super(PartiteLista,self).get_queryset()
        qs = base_qs.order_by('data')
        if self.mie:
            return qs.filter(Q(squadra1__giocatore1=self.request.user)|Q(squadra1__giocatore2=self.request.user)|Q(squadra2__giocatore1=self.request.user)|Q(squadra2__giocatore2=self.request.user))
        else:
            return qs


class PreferenzeUtenteModifica(UpdateView):
    model = PreferenzeUtente
    fields = ['iscritto']
    
    def get_object(self):
        utente, created = PreferenzeUtente.objects.get_or_create(user=self.request.user)
        return utente
            
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PreferenzeUtenteModifica, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('torneo:index')#,kwargs={'idsquadra':self.get_object().id})


class GiocatoriLista(ListView):
    model = User

    def get_queryset(self):
        base_qs = super(GiocatoriLista, self).get_queryset()
        return base_qs.filter(preferenze__iscritto=True).order_by('last_name','first_name')

class GiocatoriModifica(UpdateView):
    model = User
    fields = ['first_name','last_name']

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('torneo:giocatori')
