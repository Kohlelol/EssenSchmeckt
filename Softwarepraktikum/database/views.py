from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.contrib import messages
# Create your views here.


# Define the hierarchy
PERMISSION_HIERARCHY = {
    'management': ['management', 'Gruppenleiter', 'Standortleiter'],
    'Standortleiter': ['Standortleiter', 'Gruppenleiter'],
    'Gruppenleiter': [],

}


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
    person = person.objects.all()
    input_list = [person.id for person in person]
    duplicates = []
    seen = set()
    for item in input_list:
        if item in seen:
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.add(item)

    person = person.objects.filter(id__in=duplicates)
    return person

@login_required(login_url='/users/login/')
@group_required('groupleader')
def database_list(request):
    query = request.GET.get('q', '')
    
    if request.user.is_superuser:
        allowed_group_ids = group.objects.values_list('group_id', flat=True)
    else:
        logged_in_person = get_object_or_404(person, user=request.user)
        allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)

    else:
        persons = person.objects.filter(group_id__in=allowed_group_ids)

    group_leaders = person.objects.filter(Q(group_leaderships__group_id__in=allowed_group_ids)).distinct()

    combined_persons = persons.union(group_leaders).order_by('last_name', 'first_name')

    allowed_group_names = group.objects.filter(group_id__in=allowed_group_ids)

    for person_instance in combined_persons:
        person_instance.food_for_today = person_instance.get_food_for_today()

    return render(request, 'database/database_list.html', {'person': combined_persons, 'groups': allowed_group_names})


@login_required(login_url='/users/login/')
@group_required('groupleader')
def fetch_persons(request):
    query = request.GET.get('q', '')
    group_id = request.GET.get('group', '')
    
    if request.user.is_superuser:
        allowed_group_ids = group.objects.values_list('group_id', flat=True)
    else:
        logged_in_person = get_object_or_404(person, user=request.user)
        allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)
    else:
        persons = person.objects.filter(group_id__in=allowed_group_ids)

    if group_id:
        print(group_id)
        persons = persons.filter(group_id=group_id)

    group_leaders = person.objects.filter(Q(group_leaderships__group_id__in=allowed_group_ids)).distinct()
     
    combined_persons = persons.union(group_leaders).order_by('last_name', 'first_name')

    for person_instance in combined_persons:
        person_instance.food_for_today = person_instance.get_food_for_today()
        # if person_instance.food_for_today:
        #     print(person_instance.food_for_today.food)

    return render(request, 'database/person_list.html', {'person': combined_persons})                                                          

@login_required(login_url='/users/login/')
def set_food(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            person_id = data.get('person_id')
            food_value = data.get('food_value')
            person_instance = get_object_or_404(person, id=person_id)
            current_date = datetime.now().date()
            
            if int(food_value) == 1:
                food_instance = food.objects.filter(person=person_instance, date=current_date).first()
                if food_instance:
                    food_instance.delete()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': 'Food order not found for the given person and date'})
            else:
                food_instance, _ = food.objects.get_or_create(person=person_instance, date=current_date)
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
    logged_in_person = get_object_or_404(person, user=request.user)
    allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids).order_by('last_name')
    else:
        persons = person.objects.filter(group_id__in=allowed_group_ids).order_by('last_name')

    allowed_group_names = group.objects.filter(group_id__in=allowed_group_ids).values_list('group_name', flat=True)

    return render(request, 'database/attendance.html', {'person': persons, 'groups': allowed_group_names})


def daily_order(request):
    return render(request, 'database/daily_order.html')


def edit_orders(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(person, user=request.user)
    if request.user.is_superuser:
        allowed_group_ids = group.objects.values_list('group_id', flat=True)
    else:
        allowed_facility_id = logged_in_person.group.facility_id()
        allowed_group_ids = allowed_facility_id.groups.values_list('group_id', flat=True)

    
    if query:
        persons = person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids).order_by('last_name')
    else:
        persons = person.objects.filter(group_id__in=allowed_group_ids).order_by('last_name')

    return render(request, 'database/edit_orders.html', {'person': persons})


@login_required(login_url='/users/login/')
@group_required('groupleader')
def order(request):
    query = request.GET.get('q', '')
    logged_in_person = get_object_or_404(person, user=request.user)
    allowed_group_ids = logged_in_person.group_leaderships.values_list('group_id', flat=True)
    
    if query:
        persons = person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)
    else:
        persons = person.objects.filter(group_id__in=allowed_group_ids)

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
            person = person.objects.get(id=qr_data)

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

@login_required
@group_required('facility_manager')
def setsubstitute(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        person_id = request.POST.get('person_id')
        expire_date = request.POST.get('expire_date')
        
        groupleader_instance = groupleader.objects.create(group_id=group_id, person_id=person_id, expires=expire_date)
        
        try:
            groupleader_instance.save()
        except IntegrityError:
            return render(request, 'database/setsubstitute.html', {'error': 'Integrity error: Duplicate entry'})
        
        
        return render(request, 'database/setsubstitute.html', {'success': 'Substitute set'})
    
    # query = request.GET.get('q', '')
    # if request.user.is_superuser:
    #     facility_id = facility.objects.values_list('facility_id', flat=True)
    # else:
    #     logged_in_person = get_object_or_404(person, user=request.user)
    #     facility_id = logged_in_person.group.facility_id
    
    all_groupleaders = groupleader.objects.all().values_list('person_id', flat=True)
    groupleaders = person.objects.filter(id__in=all_groupleaders)
    # if query:
    #     groupleaders = person.objects.filter(
    #         (Q(first_name__icontains=query) | Q(last_name__icontains=query)), id__in=all_groupleaders)
    # else:
    #     groupleaders = person.objects.filter(id__in=all_groupleaders)

    # groups = group.objects.filter(facility_id=facility_id)
    groups = group.objects.all()
    
    groupleader_instances = groupleader.objects.all()
    
    return render(request, 'database/setsubstitute.html', {'groupleaders': groupleaders, 'groups': groups, 'groupleader_instances': groupleader_instances})

@login_required
@group_required('management')
def create_accounts(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        person_id = request.POST.get('person_id')
        permission_groups = request.POST.getlist('permission_groups')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            except IntegrityError:
                messages.error(request, 'Username already exists.')
                return redirect('database:create_accounts')
            
            for permission_group in permission_groups:
                group = Group.objects.get(name=permission_group)
                user.groups.add(group)
            
            if person_id:
                person_instance = person.objects.get(id=person_id)
                if person_instance.user:
                    messages.error(request, 'Account already exists for the given person.')
                    return redirect('database:create_accounts')
                person_instance.user = user
                person_instance.save()
            
            messages.success(request, 'Account created successfully.')
            return redirect('database:create_accounts')

    groups = Group.objects.all()
    
    if request.user.is_superuser:
        assignable_groups = [group.name for group in groups]
    else:
        user_groups = request.user.groups.values_list('name', flat=True)
        assignable_groups = set()
        for user_group in user_groups:
            assignable_groups.update(PERMISSION_HIERARCHY.get(user_group, []))
    
    if request.user.is_superuser | request.user.groups.filter(name='management').exists():
        assignable_persons = person.objects.all()
    else:
        logged_in_person = get_object_or_404(person, user=request.user)
        facility_id = logged_in_person.group.facility_id
        assignable_persons = person.objects.filter(group__facility_id=facility_id)
    
    return render(request, 'database/create_accounts.html', {'persons': assignable_persons, 'groups': groups, 'assignable_groups': assignable_groups})

@login_required
@group_required('management')
def create_person(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        group_id = request.POST.get('group_id')

        if not first_name or not last_name:
            messages.error(request, 'Please fill in all required fields.')
        else:
            person = person(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)
            if group_id:
                person.group_id_id = group_id
            person.save()
            messages.success(request, 'person created successfully.')
            return redirect('database:create_person')

    groups = group.objects.all()
    return render(request, 'database/create_person.html', {'groups': groups})