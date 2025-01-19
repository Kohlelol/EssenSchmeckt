from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from collections import defaultdict
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

    group_leaders = person.objects.filter((Q(first_name__icontains=query) | Q(last_name__icontains=query)), Q(group_leaderships__group_id__in=allowed_group_ids)).distinct()

    combined_persons = persons.union(group_leaders).order_by('last_name', 'first_name')

    allowed_group_names = group.objects.filter(group_id__in=allowed_group_ids)

    for person_instance in combined_persons:
        person_instance.food_for_today = person_instance.get_food_for_today()        
        
    current_date = datetime.now().date()
    latest_pdf = PDFDocument.objects.filter(from_date__lte=current_date, expire_date__gte=current_date).order_by('-uploaded_at').first()

    return render(request, 'database/database_list.html', {'person': combined_persons, 'groups': allowed_group_names, 'latest_pdf': latest_pdf})


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

    group_leaders = person.objects.filter((Q(first_name__icontains=query) | Q(last_name__icontains=query)), Q(group_leaderships__group_id__in=allowed_group_ids)).distinct()
     
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


def person_group_management(request):
    persons = person.objects.all()
    groups = group.objects.all()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if  form_type == 'assign_group':
            person_id = request.POST.get('person_id')
            group_id = request.POST.get('group_id')
            person_instance = get_object_or_404(person, id=person_id)
            person_instance.group_id_id = group_id
            person_instance.save()

    return render(request, 'database/person_group_management.html', {'person': persons, 'groups': groups})

@login_required(login_url='/users/login/')
@group_required('management')
def fetch_person_group(request):
    print("fetch_person_group started")
    query = request.GET.get('q', '')
    group_id = request.GET.get('group', '')
    
    allowed_group_ids = group.objects.values_list('group_id', flat=True)
    
    if query:
        persons = person.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)), group_id__in=allowed_group_ids)
    else:
        persons = person.objects.all()

    if group_id:
        if group_id == 'None':
            group_id = None
        persons = persons.filter(group_id=group_id)
        
    all_groups = group.objects.all()
    print("render started")
    return render(request, 'database/group_list.html', {'person': persons, 'all_groups': all_groups})  

@login_required(login_url='/users/login/')
@group_required('management')
def set_group(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            person_id = data.get('person_id')
            food_value = data.get('group_id')
            person_instance = get_object_or_404(person, id=person_id)
                        
            # if int(food_value) == 1:
            #     food_instance = food.objects.filter(person=person_instance, date=current_date).first()
            #     if food_instance:
            #         food_instance.delete()
            #         return JsonResponse({'success': True})
            #     else:
            #         return JsonResponse({'success': False, 'error': 'Food order not found for the given person and date'})
            # else:
            #     food_instance, _ = food.objects.get_or_create(person=person_instance, date=current_date)
            #     food_instance.food = food_value
            #     food_instance.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def create_facility_group(request):
    groups = group.objects.all()
    facilites = facility.objects.all()
    form_type = request.POST.get('form_type')
    if request.method == 'POST':
        if form_type == 'create_group':
            group_name = request.POST.get('group_name')
            facility_id = request.POST.get('facility_id')
            task = request.POST.get('group_task')
            try:
                group_instance = group(group_name=group_name, facility_id=facility_id, task=task)
                group_instance.save()
            except IntegrityError:
                error = {'form_type': 'create_group', 'message': 'Group creation failed'}
                return render(request, 'database/create_facility_group.html', {'error': error})
            
            previous_page = request.META.get('HTTP_REFERER', '/')
            success_url = f"{reverse('database:success')}?message=Group Successfully assigned&previous_page={previous_page}"
        
            return redirect(success_url) 
        
        if form_type == 'create_facility':
            facility_name = request.POST.get('facility_name')
            facility_location = request.POST.get('facility_location')
            try: 
                facility_instance = facility(facility_name=facility_name, facility_location=facility_location)
                facility_instance.save()
            except IntegrityError:
                error = {'form_type': 'create_facility', 'message': 'Facility creation failed'}
                return render(request, 'database/create_facility_group.html', {'error': error})
            
            previous_page = request.META.get('HTTP_REFERER', '/')
            success_url = f"{reverse('database:success')}?message=Group Successfully assigned&previous_page={previous_page}"
        
            return redirect(success_url) 
        
    return render(request, 'database/create_facility_group.html', {'groups': groups, 'facilities': facilites})


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
            person_instance = person.objects.get(id=qr_data)

            food_instance = food.objects.filter(date=current_date, person=person).first()
            if food_instance:
                if food_instance.served:
                    return render(request, 'database/decode_qr.html', {'success': True, 'person': person_instance, 'food': 'Food already served for the given person and date'})
                return render(request, 'database/decode_qr.html', {'success': True, 'person': person_instance, 'food': food_instance.food + ' marked as served'})
            else:
                return render(request, 'database/decode_qr.html', {'success': True, 'person': person_instance, 'food': 'No food order found for the given person and date'})

        except Exception as e:
            return render(request, 'database/decode_qr.html', {'success': False, 'error': str(e)})
        
    return render(request, 'database/decode_qr.html', {'success': False, 'error': 'Invalid request method'})

def setgroupleader(request):
    return render(request, 'database/setgroupleader.html')

@login_required
@group_required('facility_manager')
def setsubstitute(request):
        # query = request.GET.get('q', '')
    # if request.user.is_superuser:
    #     facility_id = facility.objects.values_list('facility_id', flat=True)
    # else:
    #     logged_in_person = get_object_or_404(person, user=request.user)
    #     facility_id = logged_in_person.group.facility_id
    
    # all_groupleaders = groupleader.objects.all().values_list('person_id', flat=True)
    # groupleaders = person.objects.filter(id__in=all_groupleaders)
    # if query:
    #     groupleaders = person.objects.filter(
    #         (Q(first_name__icontains=query) | Q(last_name__icontains=query)), id__in=all_groupleaders)
    # else:
    #     groupleaders = person.objects.filter(id__in=all_groupleaders)

    # groups = group.objects.filter(facility_id=facility_id)
    groups = group.objects.all()
    
    groupleader_instances = groupleader.objects.all()
    
    # not_groupleaders_with_account = person.objects.exclude(id__in=all_groupleaders) # everyone with account, but not currently groupleader of a group
    # not_groupleaders_with_account = not_groupleaders_with_account.exclude(user=None)
    
    list_type = request.GET.get('list_type')
    all_groupleaders = groupleader.objects.all().values_list('person_id', flat=True)
    
    if list_type == 'groupleaders':
        persons = person.objects.filter(id__in=all_groupleaders)
        groupleader_users = User.objects.filter(groups__name='groupleader')
        groupleader_persons = person.objects.filter(user__in=groupleader_users)
        persons = persons.union(groupleader_persons).order_by('last_name', 'first_name')
    else:
        groupleader_user_role = User.objects.filter(groups__name='groupleader')
        persons = person.objects.exclude(id__in=all_groupleaders).exclude(user=None).exclude(user__in=groupleader_user_role).order_by('last_name', 'first_name')
    
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        person_id = request.POST.get('person_id')
        expire_date = request.POST.get('expire_date')
        if person_id == "":
            return render(request, 'database/setsubstitute.html', {'error': 'Please select a person', 'groupleaders': list(persons.values('id', 'first_name', 'last_name')), 'groups': groups, 'groupleader_instances': groupleader_instances})
        person_instance = get_object_or_404(person, id=person_id)
        user = person_instance.user
        if expire_date == "":
            expire_date = None
        if user:
            groupleader_group, created = Group.objects.get_or_create(name='groupleader')
            if not user.groups.filter(name='groupleader').exists():
                user.groups.add(groupleader_group)

        
        try:
            groupleader_instance = groupleader.objects.create(group_id=group_id, person_id=person_id, expires=expire_date)
            groupleader_instance.save()
        except IntegrityError:
            return render(request, 'database/setsubstitute.html', {'error': 'Integrity error: Duplicate entry', 'groupleaders': list(persons.values('id', 'first_name', 'last_name')), 'groups': groups, 'groupleader_instances': groupleader_instances})
        
        
        return render(request, 'database/setsubstitute.html', {'success': 'Substitute set', 'groupleaders': list(persons.values('id', 'first_name', 'last_name')), 'groups': groups, 'groupleader_instances': groupleader_instances})

    return render(request, 'database/setsubstitute.html', {'groupleaders': list(persons.values('id', 'first_name', 'last_name')), 'groups': groups, 'groupleader_instances': groupleader_instances})

@login_required
def fetch_groupleaders(request):
    list_type = request.GET.get('list_type')
    all_groupleaders = groupleader.objects.all().values_list('person_id', flat=True)
    
    if list_type == 'groupleaders':
        persons = person.objects.filter(id__in=all_groupleaders)
        groupleader_users = User.objects.filter(groups__name='groupleader')
        groupleader_persons = person.objects.filter(user__in=groupleader_users)
        persons = persons.union(groupleader_persons).order_by('last_name', 'first_name')
    else:
        groupleader_user_role = User.objects.filter(groups__name='groupleader')
        persons = person.objects.exclude(id__in=all_groupleaders).exclude(user=None).exclude(user__in=groupleader_user_role).order_by('last_name', 'first_name')
    
    persons_data = [{'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name} for person in persons]
    return JsonResponse(persons_data, safe=False)

@login_required
@group_required('management')
def create_accounts(request):
    
    if request.user.is_superuser:
        assignable_groups = Group.objects.all()
    else:
        user_groups = request.user.groups.values_list('name', flat=True)
        assignable_groups = set()
        # for user_group in user_groups:
        #     assignable_groups.update(PERMISSION_HIERARCHY.get(user_group, []))
        assignable_groups = Group.objects.filter(name__in=set().union(*[PERMISSION_HIERARCHY.get(group, []) for group in user_groups]))
    
    if request.user.is_superuser or request.user.groups.filter(name='management').exists():
        assignable_persons = person.objects.exclude(user__isnull=False)
    else:
        logged_in_person = get_object_or_404(person, user=request.user)
        facility_id = logged_in_person.group.facility_id
        assignable_persons = person.objects.filter(group__facility_id=facility_id)
        assignable_persons = assignable_persons.exclude(user__isnull=False)
    
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
                return render(request, 'database/create_accounts.html', {
                        'persons': assignable_persons,
                        'assignable_groups': assignable_groups,
                        'next': request.POST.get('next', '')
                    })
            
            for permission_group in permission_groups:
                group = Group.objects.get(name=permission_group)
                user.groups.add(group)
                if permission_group == 'admin':
                    user.is_superuser = True
            
            if person_id:
                person_instance = person.objects.get(id=person_id)
                if person_instance.user:
                    messages.error(request, 'Account already exists for the given person.')
                    # return redirect('database:create_accounts')
                    return render(request, 'database/create_accounts.html', {
                        'persons': assignable_persons,
                        'assignable_groups': assignable_groups,
                        'next': request.POST.get('next', '')
                    })
                person_instance.user = user
                person_instance.save()
            
            messages.success(request, 'Account created successfully.')
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            
            return redirect('database:create_accounts')

    return render(request, 'database/create_accounts.html', {'persons': assignable_persons, 'assignable_groups': assignable_groups, 'next': request.POST.get('next', '')})


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
            if date_of_birth == "":
                date_of_birth = None
            person_instance = person(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)
            if group_id:
                person_instance.group_id_id = group_id
            person_instance.save()
            messages.success(request, 'person created successfully.')
            return redirect('database:create_person')

    groups = group.objects.all()
    return render(request, 'database/create_person.html', {'groups': groups})


@login_required
@group_required('group_leader')
def upload_menu(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        expire_date = request.POST.get('expire_date')
        from_date = request.POST.get('from_date')
        
        fs = FileSystemStorage(location='media/menu')
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        
        PDFDocument.objects.create(file='menu/' + filename, expire_date=expire_date, from_date=from_date)
        
        previous_page = request.META.get('HTTP_REFERER', '/')
        success_url = f"{reverse('database:success')}?message=PDF erfolgreich hochgeladen&previous_page={previous_page}"
        
        return redirect(success_url) 
    
    return render(request, 'database/upload_menu.html')

def success(request):
    message = request.GET.get('message', 'Operation completed successfully.')
    previous_page = request.GET.get('previous_page', '/')
    return render(request, 'database/success.html', {'message': message, 'previous_page': previous_page})

@login_required(login_url='/users/login/')
def init_export_order(request):
    if request.method == 'POST':
        lock_items = request.POST.get('lock_items')
        current_time = datetime.now().time()
        if lock_items and current_time > datetime.strptime('08:00', '%H:%M').time():
            food.objects.filter(date=datetime.now().date()).update(locked=True)
            print("Items locked successfully.")
            return redirect('database:export_order')

        print("Locking failed. Please try again later.")
        return render(request, 'database/init_export_order.html', {'error': 'Locking failed. Please try again later.'})

    return render(request, 'database/export_order.html')    


@login_required(login_url='/users/login/')
@group_required('management')
def export_order(request):
    persons = person.objects.all().order_by('last_name', 'first_name')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 40, "Food Orders for Today")

    # Table headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 80, "First Name")
    p.drawString(150, height - 80, "Last Name")
    p.drawString(250, height - 80, "Group")
    p.drawString(350, height - 80, "Order")


    p.setFont("Helvetica", 12)
    y = height - 100
    order_totals = defaultdict(lambda: defaultdict(int))

    for person_instance in persons:
        p.drawString(50, y, person_instance.first_name)
        p.drawString(150, y, person_instance.last_name)
        p.drawString(250, y, person_instance.group_id.group_name)
        person_food = person_instance.get_food_for_today()
        if person_food:
            food_string = "Rot" if person_food.food == 2 else "Blau"
            if person_instance.group_id is None or person_instance.group_id.facility_id is None:
                facility_name = 'Unknown'
            else:
                facility_name = person_instance.group_id.facility_id.facility_name
            order_totals[facility_name][food_string] += 1
        else:
            food_string = 'Keine Bestellung'
        p.drawString(350, y, str(food_string))
        y -= 20
        if y < 40:  # Check if we need to create a new page
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 40

    # Add totals to the PDF
    p.showPage()
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 40, "Order Totals by Facility")

    p.setFont("Helvetica-Bold", 12)
    y = height - 80
    for facility, orders in order_totals.items():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, str(facility))
        y -= 20
        for order, count in orders.items():
            p.setFont("Helvetica", 12)
            p.drawString(100, y, f"{order}: {count}")
            y -= 20
            if y < 40:  # Check if we need to create a new page
                p.showPage()
                p.setFont("Helvetica", 12)
                y = height - 40

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response