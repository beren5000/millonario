from django import template
register = template.Library()
def mod(value, arg):
    return value % arg
register.filter('mod', mod)