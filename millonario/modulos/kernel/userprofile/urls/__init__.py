from django.conf import settings

if hasattr(settings, "I18N_URLS") and settings.I18N_URLS:
    try:
        module = __import__("millonario.modulos.kernel.userprofile.urls.%s" % (settings.LANGUAGE_CODE), \
                            {}, {}, "urlpatterns")
        globals().update({ "urlpatterns": module.__dict__["urlpatterns"] })
    except:
        module = __import__("millonario.modulos.kernel.userprofile.urls.en", {}, {}, "urlpatterns")
        globals().update({ "urlpatterns": module.__dict__["urlpatterns"] })
else:
    module = __import__("millonario.modulos.kernel.userprofile.urls.en", {}, {}, "urlpatterns")
    globals().update({ "urlpatterns": module.__dict__["urlpatterns"] })
