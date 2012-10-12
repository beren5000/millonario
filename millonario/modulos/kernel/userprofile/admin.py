from django.contrib import admin
from millonario.modulos.kernel.userprofile.models import EmailValidation, Avatar

class EmailValidationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('user__username', 'user__first_name')


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','image')
    search_fields = ('user__username', 'user__first_name')
    raw_id_fields = ['user']

admin.site.register(Avatar,AvatarAdmin)
admin.site.register(EmailValidation, EmailValidationAdmin)
