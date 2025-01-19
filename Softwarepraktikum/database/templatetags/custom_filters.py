from django import template

register = template.Library()

@register.filter
def any_locked(person_list):
    return any(person.food_for_today and person.food_for_today.locked for person in person_list)