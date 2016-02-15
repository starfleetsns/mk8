from django.shortcuts import render,get_object_or_404,redirect

from django.http import HttpResponse,Http404

from torneo.models import Squadra,Partita

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

def squadre(request):
    lista = Squadra.objects.order_by('nome').all()
    return render(request,'torneo/squadre.html',{'lista':lista})

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
        }
    if 'splash' not in request.session:
        request.session['splash'] = False
        context['animazione'] = True
    else:
        context['animazione'] = False

    return render(request,'torneo/index.html',context)

def regolamento(request):
    return render(request,'torneo/regolamento.html')


    

