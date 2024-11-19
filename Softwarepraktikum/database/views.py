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
@group_required('')
def database_list(request):
    person = Person.objects.all().order_by('last_name')
    return render(request, 'database/database_list.html', {'person': person})


