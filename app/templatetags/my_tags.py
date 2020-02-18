from django import template

register = template.Library()


@register.filter
def fields_name(obj):
    return [x.attname for x in obj._meta.fields]


@register.filter
def fields_attr(obj):
    f_name = [x.attname for x in obj._meta.fields]
    return [getattr(obj, f) for f in f_name]
