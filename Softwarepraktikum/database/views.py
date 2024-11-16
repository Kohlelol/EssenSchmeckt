from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Person
# Create your views here.

@login_required(login_url='/users/login/')
def database_list(request):
    person = Person.objects.all().order_by('last_name')
    return render(request, 'database/database_list.html', {'person': person})

