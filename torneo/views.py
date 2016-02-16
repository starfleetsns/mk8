from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import ListView
from torneo.models import Squadra,Partita
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.exceptions import PermissionDenied

import re

# Create your views here.

def squadreid(request,idsquadra):
    squadra = get_object_or_404(Squadra,pk=idsquadra)
    partite = squadra.partite()
    return render(request,'torneo/squadreid.html',{'squadra':squadra,'partite':partite})

def classifica(request):
    squadre = Squadra.objects.order_by('-punteggio').all()
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
        'nsquadre': Squadra.objects.count(),
        'npartite':  Partita.objects.count(),
        'npartitedone' : Partita.objects.filter(done=True).count(),
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
    fields = ['giocatore1','giocatore2','immagine','owner']
    success_url = '/torneo/squadre/'
    
    # def get_queryset(self):
    #     base_qs = super(SquadreModifica, self).get_queryset()
    #     if self.request.user.is_superuser or self.request.user.has_perm('torneo.change_squadra'):
    #         return base_qs
    #     else:
    #         if base_qs is None:
    #             return base_qs
    #         else:
    #             return base_qs.filter(owner=self.request.user)

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

class SquadreLista(ListView):
    model = Squadra
    mie = False

    def get_queryset(self):
        base_qs = super(SquadreLista,self).get_queryset()
        if self.mie:
            return base_qs.filter(owner=self.request.user)
        else:
            return base_qs


