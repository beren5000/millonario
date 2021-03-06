from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib.auth.views import  login
from millonario.modulos.kernel.userprofile.views import *

urlpatterns = patterns('',
    # Private profile
    url(r'^consultar/usuarios/cedula/$', consultar_usuario_cedula, name='consultar_usuario_cedula' ),
    url(r'^referencias/(?P<referencia_id>\d+)$', referencias, name='referencias'),
    url(r'^reconfirmar-perfil/$', reconfirmar_perfil, name='reconfirmar_perfil'),
    url(r'^perfil/$', overview, name='profile_overview'),

    url(r'^perfil/mis-jugadas/$', mis_jugadas, name='profile_mis_jugadas'),
    url(r'^perfil/mis-premios/$', mis_premios, name='profile_mis_premios'),

    url(r'^perfil/editar/ubicacion/$', location, name='profile_edit_location'),

    url(r'^perfil/editar/ubicacion/listo/$', direct_to_template,
        {'extra_context': {'section': 'location'},
        'template': 'userprofile/profile/location_done.html'},
        name='profile_edit_location_done'),

    url(r'^perfil/editar/personal/$', personal, name='profile_edit_personal'),

    url(r'^perfil/editar/personal/listo/$', direct_to_template,
        {'extra_context': {'section': 'personal'},
        'template': 'userprofile/profile/personal_done.html'},
        name='profile_edit_personal_done'),

    url(r'^perfil/eliminar/$', delete, name='profile_delete'),

    url(r'^perfil/eliminar/listo/$', direct_to_template,
        {'extra_context': {'section': 'delete'},
        'template': 'userprofile/profile/delete_done.html'},
        name='profile_delete_done'),

    url(r'^perfil/obtener_infopais/(?P<lat>[0-9\.\-]+)/(?P<lng>[0-9\.\-]+)/$',
        fetch_geodata,
        name='profile_geocountry_info'),

    # Avatars
    url(r'^perfil/editar/avatar/eliminar/$', avatardelete,
        name='profile_avatar_delete'),

    url(r'^perfil/editar/avatar/$', avatarchoose, name='profile_edit_avatar'),

    url(r'^perfil/editar/avatar/buscar/$', searchimages,
        name='profile_avatar_search'),

    url(r'^perfil/editar/avatar/recortar/$', avatarcrop,
        name='profile_avatar_crop'),

    url(r'^perfil/edit/avatar/recortar/listo/$', direct_to_template,
        { 'extra_context': {'section': 'avatar'},
        'template': 'userprofile/avatar/done.html'},
        name='profile_avatar_crop_done'),

    # Account utilities
    url(r'^email/validar/$', email_validation, name='email_validation'),

    url(r'^email/validar/procesado/$', direct_to_template,
        {'template': 'userprofile/account/email_validation_processed.html'},
        name='email_validation_processed'),

    url(r'^email/validar/(?P<key>.{70})/$', email_validation_process,
        name='email_validation_process'),

    url(r'^email/validar/reestablecer/$', email_validation_reset,
        name='email_validation_reset'),

    url(r'^email/validar/reestablecer/(?P<action>listo|fallo)/$',
        direct_to_template,
        {'template' : 'userprofile/account/email_validation_reset_response.html'},
        name='email_validation_reset_response'),

    url(r'^contrasena/reestablecer/$',
        'django.contrib.auth.views.password_reset',
        {'template_name': 'userprofile/account/password_reset.html',
         'email_template_name': 'userprofile/email/password_reset_email.txt' },
        name='password_reset'),

    url(r'^password/reestablecer/listo/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'userprofile/account/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^password/cambiar/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'userprofile/account/password_change.html'},
        name='password_change'),

    url(r'^password/cambiar/listo/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'userprofile/account/password_change_done.html'},
        name='password_change_done'),

    url(r'^reestablecer/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'userprofile/account/password_reset_confirm.html'},
        name="password_reset_confirm"),

    url(r'^reestablecer/listo/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'userprofile/account/password_reset_complete.html'},
        name="password_reset_complete"),

    url(r'^entrar/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'),

    url(r'^salir/$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'},
        name='logout'),

    # Registration
    url(r'^ciudad/(?P<id_departamento>[a-z|0-9|\w]+)/$', ajax_form_ciudad, name='ajax_form_ciudad'),

    url(r'^registro/$', register, name='register'),
    #url(r'^registro-demo/$', direct_to_template, {'template' : '100marcas/cuenta/registrodemo.php'}, name='first_step'), 
    #url(r'^registro/$', first_step_register, name='signup'),
    #url(r'^registro-segundo-paso/$', second_step_register, name='second_step'),
    #url(r'^registro-tercer-paso/$', third_step_register, name='third_step'),
    #url(r'^registro-cuarto-paso/$', fourth_step_register, name='fourth_step'),
    
    
    #url(r'^invitados/(?P<inviter_key>.{70})/$', inviter_first_step_register, name='inviter_signup'),

    url(r'^registro/validar/$', direct_to_template,
        {'template' : 'userprofile/account/validate.html'},
        name='signup_validate'),

    url(r'^registro/completo/$', direct_to_template,
        {'template': 'modulos/userprofile/account/registration_done.html'},
        name='signup_complete'),

    # Users public profile
    url(r'^perfil/(?P<username>.+)/$', public, name='profile_public'),
    
    url(r'^mispuntos/$', mispuntos, name='mispuntos'),
    url(r'^infohijo/(?P<id_hijo>.+)/$', infohijo, name='infohijo'),
    url(r'^matarhijo/(?P<id_hijo>.+)/$', matarhijo, name='matarhijo'),

)
