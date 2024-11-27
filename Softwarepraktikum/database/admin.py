from django.contrib import admin
from .models import Person, food, group, groupleader, facility, facility_manager

# Register your models here.
admin.site.register(Person)
admin.site.register(food)
admin.site.register(group)
admin.site.register(groupleader)
admin.site.register(facility)
admin.site.register(facility_manager)