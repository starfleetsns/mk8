from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.views.generic.edit import CreateView,UpdateView,DeleteView,ModelFormMixin
from django.views.generic import ListView
from torneo.models import Squadra,Partita
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
#from django.forms import ModelForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied


# Create your views here.

def squadreid(request,idsquadra):
    squadra = get_object_or_404(Squadra,pk=idsquadra)
    partite = squadra.partite()
    return render(request,'torneo/squadreid.html',{'squadra':squadra,'partite':partite})

def classifica(request):
    squadre = Squadra.objects.filter(confermata=True).order_by('-punteggio').all()
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

def index(request):
    context = {
        'nsquadre': Squadra.objects.filter(confermata=True).count(),
        'npartite':  Partita.objects.count(),
        'npartitedone' : Partita.objects.filter(stato=Partita.DONE).count(),
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
    fields = ['nome','giocatore1','giocatore2','immagine']
    success_url = '/torneo/squadre/'
    
#    @method_decorator(login_required)
    def form_valid(self,form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        form.instance.owner = self.request.user
        return super(SquadreNuova, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SquadreNuova, self).dispatch(*args, **kwargs)
    

class SquadreModifica(UpdateView):
    model = Squadra
    fields = ['giocatore1','giocatore2','immagine']
    
    def get_object(self):
        squadra = super(SquadreModifica, self).get_object()
        if self.request.user.is_superuser or self.request.user.has_perm('torneo.change_squadra'):
            return squadra
        else:
            if squadra.owner == self.request.user:
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
#            if squadra.owner == self.request.user:
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
            return qs.filter(owner=self.request.user)
        else:
            return qs


class PartiteModifica(UpdateView):
    model = Partita
    fields = ['data','punteggio11','punteggio12','punteggio21','punteggio22']
#    form_class =  modelform_factory(Kunde, widgets={"data": SelectDateWidget })
    
    
    def get_object(self):
        partita = super(PartiteModifica, self).get_object()
        if partita.stato != Partita.INCOGNITA:
            if (partita.squadra1.owner == self.request.user) and (partita.stato == Partita.ATTESA2):
                return partita
            elif (partita.squadra2.owner == self.request.user) and (partita.stato == Partita.ATTESA1):
                return partita
            else:
                raise PermissionDenied
        if (partita.squadra1.owner == self.request.user) or (partita.squadra2.owner == self.request.user):
            return partita
        else:
            raise PermissionDenied
            
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PartiteModifica, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('torneo:partitemie')

    def form_valid(self,form):
        if form.instance.squadra1.owner == self.request.user:
            if form.instance.squadra2.owner == self.request.user:
                form.instance.stato=Partita.DONE
                for squadra in Squadra.objects.all():
                    squadra.ripunteggia()
            else:
                form.instance.stato=Partita.ATTESA2
        elif form.instance.squadra2.owner == self.request.user:
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
        if (partita.squadra1.owner == self.request.user) and (partita.stato == Partita.ATTESA1):
            return partita
        elif (partita.squadra2.owner == self.request.user) and (partita.stato == Partita.ATTESA2):
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
            for squadra in Squadra.objects.all():
                squadra.ripunteggia()
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
            return qs.filter(Q(squadra1__owner=self.request.user)|Q(squadra2__owner=self.request.user))
        else:
            return qs



