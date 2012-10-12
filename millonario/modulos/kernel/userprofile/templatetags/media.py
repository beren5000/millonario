from django.conf import settings
from django import template

register = template.Library()

def media_url(url):
    return '%s%s?%s' % (settings.MEDIA_URL, url, settings.MEDIA_VERSION)

register.simple_tag(media_url)
