from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.

def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

def read_csv_csv(csvfile_path):
    import csv
    with open(csvfile_path, 'r') as file:
        reader = csv.reader(file)
        df = [row for row in reader]
        file.close()
    return df

def read_csv_pandas(csvfile_path):
    import pandas as pd
    df = pd.read_csv(csvfile_path)
    return df

def get_duplicate_persons():
    person = Person.objects.all()
    input_list = [person.id for person in person]
    duplicates = []
    seen = set()
    for item in input_list:
        if item in seen:
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.add(item)

    person = Person.objects.filter(id__in=duplicates)
    return person

@login_required(login_url='/users/login/')
@group_required('groupleader')
def database_list(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(Person, user=request.user)
    allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids)

    allowed_group_names = group.objects.filter(id__in=allowed_group_ids).values_list('name', flat=True)

    return render(request, 'database/database_list.html', {'person': persons, 'groups': allowed_group_names})

@login_required(login_url='/users/login/')
@group_required('groupleader')
def fetch_persons(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(Person, user=request.user)
    allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids)

    allowed_group_names = group.objects.filter(id__in=allowed_group_ids).values_list('name', flat=True)

    return render(request, 'person_list.html', {'person': persons, 'groups': allowed_group_names})                                                          



def attendance(request):
    query = request.GET.get('q', '')
    if query:
        logged_in_person = get_object_or_404(Person, user=request.user)
        allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), 
             group_id__in=allowed_group_ids
             )
    else:
        logged_in_person = get_object_or_404(Person, user=request.user)
        allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
        persons = Person.objects.filter(group_id__in=allowed_group_ids)
    return render(request, 'database/attendance.html', {'person': persons})


def daily_order(request):
    return render(request, 'database/daily_order.html')

def edit_orders(request):
    return render(request, 'database/edit_orders.html')

def order(request):
    return render(request, 'database/order.html')

def qr_code_scanner(request):
    return render(request, 'database/qr_code_scanner.html')

def setgroupleader(request):
    return render(request, 'database/setgroupleader.html')

def setsubstitute(request):
    return render(request, 'database/setsubstitute.html')


