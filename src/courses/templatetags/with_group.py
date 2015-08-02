from django.template import Library
register = Library()


@register.filter
def with_group(things, group):
    return things.filter(Group=group)