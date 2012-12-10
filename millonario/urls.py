from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from millonario.settings import MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'millonario.views.home', name='home'),
    # url(r'^millonario/', include('millonario.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^encuestas/', include('millonario.modulos.encuestas.urls')),
    url(r'^$', direct_to_template,
        {'template': 'index.html'},
        name='home'),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT})
)
