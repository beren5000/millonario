# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
import cPickle as pickle
import base64
from PIL import Image, ImageFilter
import os.path

from millonario.modulos.kernel.userprofile.countries import CountryField

AVATAR_SIZES = (128, 96, 64, 48, 32, 24, 16,120,160)

class BaseProfile(models.Model):
    """
    User profile model
    """

    user = models.ForeignKey(User, unique=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    country = CountryField(null=True, blank=True,default='CO')
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    
    @property
    def perfil_avatar(self):
        #return self.nombre+" " +self.apellidos
        if self.has_avatar():
            return Avatar.objects.get(user=self.user, valid=True).image.url
        else:
            if self.sexo_id == 1:
                url = '%smedia_perfil/images/female_120.png' % settings.MEDIA_URL
            else:
                url = '%smedia_perfil/images/male_120.png' % settings.MEDIA_URL
            return url
    
    class Meta:
        abstract = True

    def has_avatar(self):
        return Avatar.objects.filter(user=self.user, valid=True).count()

    def __unicode__(self):
        return _("%s's profile") % self.user

    def get_absolute_url(self):
        return reverse("profile_public", args=[self.user])


class Avatar(models.Model):
    """
    Avatar model
    """
    image = models.ImageField(upload_to="avatars/%Y/%b/%d")
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField()

    class Meta:
        unique_together = (('user', 'valid'),)

    def __unicode__(self):
        return _("%s's Avatar") % self.user

    def delete(self):
        base, filename = os.path.split(self.image.path)
        name, extension = os.path.splitext(filename)
        for key in AVATAR_SIZES:
            try:
                os.remove(os.path.join(base, "%s.%s%s" % (name, key, extension)))
            except:
                pass

        super(Avatar, self).delete()

    def save(self):
        for avatar in Avatar.objects.filter(user=self.user, valid=self.valid).exclude(id=self.id):
            base, filename = os.path.split(avatar.image.path)
            name, extension = os.path.splitext(filename)
            for key in AVATAR_SIZES:
                try:
                    os.remove(os.path.join(base, "%s.%s%s" % (name, key, extension)))
                except:
                    pass
            avatar.delete()
        super(Avatar, self).save()


class EmailValidationManager(models.Manager):
    """
    Email validation manager
    """
    def verify(self, key):
        try:
            verify = self.get(key=key)
            if not verify.is_expired():
                verify.user.email = verify.email
                verify.user.is_active = settings.ACTIVAR_USUARIO
                #############################################################
                verify.user.save()
                verify.delete()
                return True
            else:
                verify.delete()
                return False
        except:
            return False

    def getuser(self, key):
        try:
            return self.get(key=key).user
        except:
            return False

    def add(self, user, email):
        """
        Add a new validation process entry
        """
        while True:
            key = User.objects.make_random_password(70)
            try:
                EmailValidation.objects.get(key=key)
            except EmailValidation.DoesNotExist:
                self.key = key
                break


        
        current_site = Site.objects.get_current()
        subject, from_email = 'El clickmillonario.com ::Registro'  , settings.DEFAULT_FROM_EMAIL
        text_content = 'Informacion sobre las jugadas administrador'        
        # el current site tiene el dominio si necesitan el media tiene el settings.MEDIA_URL
        MEDIA_URL=settings.MEDIA_URL
        user = User.objects.get(username=str(user))
        user.username = email
        user.save()
        site_name, domain = Site.objects.get_current().name, Site.objects.get_current().domain
        perfil = user.perfil_set.all()[0]
        html_content = render_to_string('emails/registro/registro.html', { 'current_site':current_site ,'user':user,'site_name':site_name, 'domain':domain ,'MEDIA_URL':MEDIA_URL,'key':key, 'perfil' : perfil })
        msg = EmailMultiAlternatives(subject,text_content, from_email, bcc=[email])
        msg.attach_alternative(html_content, "text/html")        
        estado =msg.send(fail_silently=True)
        
        
        
        
        #body = loader.get_template(template_body).render(Context(locals()))
        #subject = loader.get_template(template_subject).render(Context(locals())).strip()
        #send_mail(subject=subject, message=body, from_email=None, recipient_list=[email],fail_silently=True)
        
        
        self.filter(user=user).delete()
        return self.create(user=user, key=key, email=email)

class EmailValidation(models.Model):
    """
    Email Validation model
    """
    user = models.ForeignKey(User, unique=True)
    email = models.EmailField(blank=True)
    key = models.CharField(max_length=70, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = EmailValidationManager()

    def __unicode__(self):
        return _("Email validation process for %(user)s") % { 'user': self.user }

    def is_expired(self):
        return (datetime.datetime.today() - self.created).days > 0

    def resend(self):
        """
        Resend validation email
        """
        
        current_site = Site.objects.get_current()
        subject, from_email = 'El clickmillonario.com ::Registro'  , settings.DEFAULT_FROM_EMAIL
        text_content = 'Informacion sobre las jugadas administrador'        
        # el current site tiene el dominio si necesitan el media tiene el settings.MEDIA_URL
        MEDIA_URL=settings.MEDIA_URL
        user = self.user
        site_name, domain = Site.objects.get_current().name, Site.objects.get_current().domain        
        
        html_content = render_to_string('emails/email_juego/letter-registro.html', { 'current_site':current_site ,'user':user,'site_name':site_name, 'domain':domain ,'MEDIA_URL':MEDIA_URL,'key':self.key, 'username' : user.username })
        
        msg = EmailMultiAlternatives(subject,text_content, from_email, bcc=[self.email])
        msg.attach_alternative(html_content, "text/html")        
        estado =msg.send(fail_silently=True)
                
        #=======================================================================
        # template_body = "userprofile/email/validation.txt"
        # template_subject = "userprofile/email/validation_subject.txt"
        # site_name, domain = Site.objects.get_current().name, Site.objects.get_current().domain
        # 
        # key = self.key
        # body = loader.get_template(template_body).render(Context(locals()))
        # subject = loader.get_template(template_subject).render(Context(locals())).strip()
        # send_mail(subject=subject, message=body, from_email=None, recipient_list=[self.email])
        #=======================================================================
        
        
        self.created = datetime.datetime.now()
        self.save()
        return True

