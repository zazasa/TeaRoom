from django.template import Library
register = Library()


@register.filter
def get_groups(things):
    return [group['Group'] for group in things.values('Group').distinct()]