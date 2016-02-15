from django.shortcuts import redirect

from django.views.generic.base import RedirectView

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mk8.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^torneo/',include('torneo.urls', namespace='torneo')),
#    url(r'^$','django.contrib.staticfiles.views.serve', kwargs= {'path':'torneo/index.html'})
    url(r'^$',RedirectView.as_view(url='torneo/',permanent=False))
)

if (settings.SERVE_MEDIA):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'MK8 administration @ starfleet'
admin.site.site_title = 'MK8 admin page'
