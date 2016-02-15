from django.shortcuts import redirect

from django.views.generic.base import RedirectView

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mk8.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^torneo/',include('torneo.urls', namespace='torneo')),
#    url(r'^$','django.contrib.staticfiles.views.serve', kwargs= {'path':'torneo/index.html'})
    url(r'^$',RedirectView.as_view(url='torneo/regolamento'))
)


admin.site.site_header = 'MK8 administration @ starfleet'
admin.site.site_title = 'MK8 admin page'
