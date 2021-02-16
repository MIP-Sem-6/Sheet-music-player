from django import template
register = template.Library()

@register.filter
def get_liked(obj,user):
    return obj.get_is_liked(user)