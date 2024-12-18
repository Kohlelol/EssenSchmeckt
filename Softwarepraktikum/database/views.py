from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
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
    
    if request.user.is_superuser:
        allowed_group_ids = group.objects.values_list('group_id', flat=True)
    else:
        logged_in_person = get_object_or_404(Person, user=request.user)
        allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids).order_by('last_name')
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids).order_by('last_name')

    allowed_group_names = group.objects.filter(group_id__in=allowed_group_ids)

    for person in persons:
        person.food_for_today = person.get_food_for_today()

    return render(request, 'database/database_list.html', {'person': persons, 'groups': allowed_group_names})

@login_required(login_url='/users/login/')
@group_required('groupleader')
def fetch_persons(request):
    query = request.GET.get('q', '')
    group_id = request.GET.get('group', '')
    
    if request.user.is_superuser:
        allowed_group_ids = group.objects.values_list('group_id', flat=True)
    else:
        logged_in_person = get_object_or_404(Person, user=request.user)
        allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids).order_by('last_name')
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids).order_by('last_name')

    if group_id:
        print(group_id)
        persons = persons.filter(group_id=group_id)

    for person in persons:
        person.food_for_today = person.get_food_for_today()
        if person.food_for_today:
            print(person.food_for_today.food)

    return render(request, 'database/person_list.html', {'person': persons})                                                          

@login_required(login_url='/users/login/')
@csrf_exempt
def set_food(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            person_id = data.get('person_id')
            food_value = data.get('food_value')
            person = get_object_or_404(Person, id=person_id)
            current_date = datetime.now().date()
            
            if int(food_value) == 1:
                food_instance = food.objects.filter(person=person, date=current_date).first()
                if food_instance:
                    food_instance.delete()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': 'Food order not found for the given person and date'})
            else:
                food_instance, created = food.objects.get_or_create(person=person, date=current_date)
                food_instance.food = food_value
                food_instance.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='/users/login/')
@group_required('groupleader')
def attendance(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(Person, user=request.user)
    allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids).order_by('last_name')
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids).order_by('last_name')

    allowed_group_names = group.objects.filter(group_id__in=allowed_group_ids).values_list('group_name', flat=True)

    return render(request, 'database/attendance.html', {'person': persons, 'groups': allowed_group_names})


def daily_order(request):
    return render(request, 'database/daily_order.html')


def edit_orders(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(Person, user=request.user)
    if request.user.is_superuser:
        allowed_group_ids = group.objects.values_list('group_id', flat=True)
    else:
        allowed_facility_id = logged_in_person.group.facility_id()
        allowed_group_ids = allowed_facility_id.groups.values_list('group_id', flat=True)

    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids).order_by('last_name')
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids).order_by('last_name')

    return render(request, 'database/edit_orders.html', {'person': persons})


@login_required(login_url='/users/login/')
@group_required('groupleader')
def order(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(Person, user=request.user)
    allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)
    else:
        persons = Person.objects.filter(group_id__in=allowed_group_ids)

    allowed_group_names = group.objects.filter(group_id__in=allowed_group_ids).values_list('group_name', flat=True)

    return render(request, 'database/order.html', {'person': persons, 'groups': allowed_group_names})


def qr_code_scanner(request):
    return render(request, 'database/qr_code_scanner.html')

# @csrf_exempt
# def decode_qr(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             qr_data = data.get('qr_data', '')
#             # Process the QR code data as needed
#             return render(request, 'database/decode_qr.html', {'success': True, 'qr_data': qr_data})
#         except Exception as e:
#             return render(request, 'database/decode_qr.html', {'success': False, 'qr_data': "Exceprion part"})
#     return render(request, 'database/decode_qr.html', {'success': False, 'qr_data': 'Invalid request method'})

@csrf_exempt
def decode_qr(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            if qr_data == '':
                return render(request, 'database/decode_qr.html', {'success': False, 'error': 'No QR data found'})
    
            current_date = datetime.now().date()
            person = Person.objects.get(id=qr_data)

            food_instance = food.objects.filter(date=current_date, person=person).first()
            if food_instance:
                if food_instance.served:
                    return render(request, 'database/decode_qr.html', {'success': True, 'person': person, 'food': 'Food already served for the given person and date'})
                return render(request, 'database/decode_qr.html', {'success': True, 'person': person, 'food': food_instance.food})
            else:
                return render(request, 'database/decode_qr.html', {'success': True, 'person': person, 'food': 'No food order found for the given person and date'})

        except Exception as e:
            return render(request, 'database/decode_qr.html', {'success': False, 'error': str(e)})
        
    return render(request, 'database/decode_qr.html', {'success': False, 'error': 'Invalid request method'})

def setgroupleader(request):
    return render(request, 'database/setgroupleader.html')


def setsubstitute(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        person_id = request.POST.get('person_id')
        try:
            groupleader.objects.get(group_id=group_id, person_id=person_id)
        except groupleader.DoesNotExist:
            return render(request, 'database/setsubstitute.html', {'error': 'Group leader does not exist'})
        
        groupleader = groupleader.objects.create(group_id=group_id, person_id=person_id)
        try:
            groupleader.save()
        except IntegrityError:
            return render(request, 'database/setsubstitute.html', {'error': 'Integrity error: Duplicate entry'})
        return render(request, 'database/setsubstitute.html', {'success': 'Substitute set'})
    
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(Person, user=request.user)
    facility_id = logged_in_person.group.facility_id
    all_groupleaders = groupleader.objects.filter(group_id__facility_id=facility_id).values_list('person_id', flat=True)

    if query:
        persons = Person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), id__in=all_groupleaders)
    else:
        persons = Person.objects.filter(id__in=all_groupleaders)

    groups = group.objects.filter(facility_id=facility_id)
    
    return render(request, 'database/setsubstitute.html', {'groupleaders': persons, 'groups': groups})

