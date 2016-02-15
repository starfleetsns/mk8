from django.conf.urls import patterns, url

from torneo import views

urlpatterns = patterns('',
                       url(r'^classifica/$',views.classifica, name='classifica'),
                       url(r'^squadre/(?P<idsquadra>\d+)/$',views.squadreid, name='squadreid'),
                       url(r'^calendario/$',views.calendario, name='calendario'),
                       url(r'^regolamento/$',views.regolamento, name='regolamento'),
                       url(r'^squadre/$',views.squadre, name='squadre'),
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
