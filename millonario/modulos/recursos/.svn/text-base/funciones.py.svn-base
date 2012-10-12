__author__ = 'juan'
from django.contrib.auth.models import User
def asignar_password():
    users = User.objects.all()
    for u in users:
        u.set_password(u.username)
        u.save()
    return 1
