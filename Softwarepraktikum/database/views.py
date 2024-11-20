from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
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


@login_required(login_url='/users/login/')
# @group_required('groupleader')
def database_list(request):
    query = request.GET.get('q')
    if query:
        person = Person.objects.filter(first_name__icontains=query) | Person.objects.filter(last_name__icontains=query)
    else:
        person = Person.objects.all()

    return render(request, 'database/database_list.html', {'person': person})

def fetch_persons(request):
    query = request.GET.get('q', '')
    if query:
        persons = Person.objects.filter(first_name__icontains=query) | Person.objects.filter(last_name__icontains=query)
    else:
        persons = Person.objects.all()
    return render(request, 'person_list.html', {'person': persons})                                                          



def attendance(request):
    return render(request, 'database/attendance.html')

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