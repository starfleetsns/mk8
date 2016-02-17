from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from torneo.models import Squadra,Partita

from torneo import views

urlpatterns = patterns('',
                       url(r'^classifica/$',views.classifica, name='classifica'),
#                       url(r'^calendario/$',views.calendario, name='calendario'),
                       url(r'^partite/(?P<pk>\d+)/modifica/$',views.PartiteModifica.as_view(),name='partitemodifica'),
                       url(r'^partite/(?P<pk>\d+)/(?P<azione>(approva|rifiuta))/$',views.PartiteApprova.as_view(),name='partiteapprova'),
                       url(r'^partite/$',views.PartiteLista.as_view(),name='partite'),
                       url(r'^partite/(?P<pk>\d+)/$',DetailView.as_view(model=Partita),name='partiteid'),
                       url(r'^partite/mie/$',views.PartiteLista.as_view(mie=True),name='partitemie'),
                       url(r'^regolamento/$',views.regolamento, name='regolamento'),
#                       url(r'^squadre/$',ListView.as_view(model=Squadra,),name='squadre'),
                       url(r'^squadre/$',views.SquadreLista.as_view(),name='squadre'),
                       url(r'^squadre/mie/$',views.SquadreLista.as_view(mie=True),name='squadremie'),
#                       url(r'^squadre/$',views.squadre, name='squadre'),
                       url(r'^squadre/(?P<idsquadra>\d+)/$',views.squadreid, name='squadreid'),
                       url(r'^squadre/(?P<pk>\d+)/modifica/$',login_required(views.SquadreModifica.as_view()), name='squadremodifica'),
                       url(r'^squadre/nuova/$',login_required(views.SquadreNuova.as_view()), name='squadrenuova'),
                       url(r'^squadre/(?P<pk>\d+)/cancella/$',login_required(views.SquadreCancella.as_view()), name='squadrecancella'),
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url(r'^$',views.index, name='index')
#                           # ex: /polls/
#                               url(r'^$', views.index, name='index'),
#                           # ex: /polls/5/
#                               url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
#                           # ex: /polls/5/results/
#                               url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
#                           # ex: /polls/5/vote/
#                               url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
                       )
