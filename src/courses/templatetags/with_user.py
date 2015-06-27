from django.template import Library
register = Library()


@register.filter
def with_user(things, user):
    return things.filter(Students=user)