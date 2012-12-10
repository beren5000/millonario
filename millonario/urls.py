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
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    (r'^quien_la_tiene_clara/', include('millonario.modulos.encuestas.urls')),
    url(r'^inicio/$', direct_to_template, {'template': 'index.html'}, name='inicio'),



    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT})
)
