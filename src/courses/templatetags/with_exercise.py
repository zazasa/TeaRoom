from django.template import Library
register = Library()


@register.filter
def with_exercise(things, exercise):
    return things.filter(Exercise=exercise)