from django.shortcuts import render
from .models import Person
# Create your views here.

def database_list(request):
    person = Person.objects.all().order_by('last_name')
    return render(request, 'database/database_list.html', {'person': person})

