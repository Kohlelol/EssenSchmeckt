from django.contrib import admin
from .models import person, food, group, groupleader, facility, facility_manager

# Register your models here.
admin.site.register(person)
admin.site.register(food)
admin.site.register(group)
admin.site.register(groupleader)
admin.site.register(facility)
admin.site.register(facility_manager)