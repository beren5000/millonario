from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from millonario.modulos.encuestas.views import *
urlpatterns = patterns('',
    url(r'^administrar/$', administrar, name='administrar'),
    url(r'^concursar/$', concursar,name='concursar'),
    url(r'^agregar_pregunta/$', agregar_pregunta, name='agregar_pregunta'),
    url(r'^eliminar_pregunta/$', eliminar_pregunta, name='eliminar_pregunta'),
    url(r'^ver_preguntas/$', ver_preguntas, name='ver_preguntas'),
    url(r'^agregar_encuesta/$', agregar_encuesta, name='agregar_encuesta'),
    url(r'^desactivar_encuestas/$', desactivar_encuesta, name='desactivar_encuesta'),
    url(r'^agregar_nivel/$', agregar_nivel, name='agregar_nivel'),
    url(r'^update/$', update, name='update'),
    url(r'^update_selects/$', update_selects, name='update_selects'),
    url(r'^xmlencuestas/$', xmlencuestas, name='xmlencuestas'),
    url(r'^userlog/$', userlog, name='userlog'),
    url(r'^userreg/$', userreg, name='userreg'),
    url(r'^xmljuego/$', xmljuego, name='xmljuego'),
#===============================================================================
# 
#    url(r'^profile/edit/location/$', location, name='profile_edit_location'),
# 
# #    url(r'^profile/edit/location/done/$', direct_to_template,
# #        {'extra_context': {'section': 'location'},
# #        'template': 'userprofile/profile/location_done.html'},
# #        name='profile_edit_location_done'),
# 
#    url(r'^profile/edit/personal/$', personal, name='profile_edit_personal'),
# 
#    url(r'^profile/edit/personal/done/$', direct_to_template,
#        {'extra_context': {'section': 'personal'},
#        'template': 'userprofile/profile/personal_done.html'},
#        name='profile_edit_personal_done'),
# 
#    url(r'^profile/delete/$', delete, name='profile_delete'),
# 
#    url(r'^profile/delete/done/$', direct_to_template,
#        {'extra_context': {'section': 'delete'},
#        'template': 'userprofile/profile/delete_done.html'},
#        name='profile_delete_done'),
#    # Avatars
#    url(r'^profile/edit/avatar/delete/$', avatardelete,
#        name='profile_avatar_delete'),
# 
#    url(r'^profile/edit/avatar/$', avatarchoose, name='profile_edit_avatar'),
# 
#    url(r'^profile/edit/avatar/search/$', searchimages,
#        name='profile_avatar_search'),
# 
#    #===========================================================================
#    # url(r'^profile/edit/avatar/crop/$', avatarcrop,
#    #    name='profile_avatar_crop'),
#    #===========================================================================
# 
#    url(r'^profile/edit/avatar/crop/done/$', direct_to_template,
#        { 'extra_context': {'section': 'avatar'},
#        'template': 'userprofile/avatar/done.html'},
#        name='profile_avatar_crop_done'),
#    url(r'^email/validar/$', email_validation, name='email_validation'),
# 
#    url(r'^email/validar/processed/$', direct_to_template,
#        {'template': 'userprofile/account/email_validation_processed.html'},
#        name='email_validation_processed'),
# 
#    url(r'^email/validar/(?P<key>.{70})/$', email_validation_process,
#        name='email_validation_process'),
# 
#    url(r'^email/validar/reset/$', email_validation_reset,
#        name='email_validation_reset'),
# 
#    url(r'^email/validar/reset/(?P<action>done|failed)/$',
#        direct_to_template,
#        {'template' : 'userprofile/account/email_validation_reset_response.html'},
#        name='email_validation_reset_response'),
# 
#    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
#        {'template_name': 'userprofile/account/password_reset.html',
#         'email_template_name': 'userprofile/email/password_reset_email.txt' },
#        name='password_reset'),
# 
#    url(r'^password/reset/done/$',
#        'django.contrib.auth.views.password_reset_done',
#        {'template_name': 'userprofile/account/password_reset_done.html'},
#        name='password_reset_done'),
# 
#    url(r'^password/change/$', 'django.contrib.auth.views.password_change',
#        {'template_name': 'userprofile/account/password_change.html'},
#        name='password_change'),
# 
#    url(r'^password/change/done/$',
#        'django.contrib.auth.views.password_change_done',
#        {'template_name': 'userprofile/account/password_change_done.html'},
#        name='password_change_done'),
# 
#    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
#        'django.contrib.auth.views.password_reset_confirm',
#        {'template_name': 'userprofile/account/password_reset_confirm.html'},
#        name="password_reset_confirm"),
# 
#    url(r'^reset/done/$',
#        'django.contrib.auth.views.password_reset_complete',
#        {'template_name': 'userprofile/account/password_reset_complete.html'},
#        name="password_reset_complete"),
# 
#    url(r'^login/$', 'django.contrib.auth.views.login',
#        {'template_name': 'userprofile/account/login.html'},
#        name='login'),
# 
#    url(r'^logout/$', 'django.contrib.auth.views.logout',
#        {'template_name': 'userprofile/account/logout.html'},
#        name='logout'),
# 
#    # Registration
#    url(r'^registrar/$', register, name='signup'),
# 
#    url(r'^registrar/validate/$', direct_to_template,
#        {'template' : 'userprofile/account/validate.html'},
#        name='signup_validate'),
# 
#    url(r'^registrar/completar/$', direct_to_template,
#        {'template': 'userprofile/account/registration_done.html'},
#        name='signup_complete'),
# 
#    # Users public profile
#===============================================================================


)
