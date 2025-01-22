from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'database'

urlpatterns = [
    path('', views.database_list, name='database_list'),
    path('attendance/', views.attendance, name='attendance'),
    path('init_export_order/', views.init_export_order, name='init_export_order'),
    path('export_order/', views.export_order, name='export_order'),
    path('person_group_management/', views.person_group_management, name='person_group_management'),
    path('order/', views.order, name='order'),
    path('qr_code_scanner/', views.qr_code_scanner, name='qr_code_scanner'),
    path('setgroupleader/', views.setgroupleader, name='setgroupleader'),
    path('setsubstitute/', views.setsubstitute, name='setsubstitute'),
    path('fetch-persons/', views.fetch_persons, name='fetch_persons'),
    path('decode_qr/', views.decode_qr, name='decode_qr'),
    path('set_food/', views.set_food, name='set_food'),
    path('create_accounts/', views.create_accounts, name='create_accounts'),
    path('create_person/', views.create_person, name='create_person'),
    path('fetch_groupleaders/', views.fetch_groupleaders, name='fetch_groupleaders'),
    path('upload_menu/', views.upload_menu, name='upload_menu'),
    path('success/', views.success, name='success'),
    path('create_facility_group/', views.create_facility_group, name='create_facility_group'),
    path('fetch-person-group/', views.fetch_person_group, name='fetch-person-group'),
    path('set_group/', views.set_group, name='set_group'),
    path('assign_account_to_person/', views.assign_account_to_person, name='assign_account_to_person'),
    path('unassign_account/', views.unassign_account, name='unassign_account'),
    path('export_qr_code/', views.export_qr_code, name='export_qr_code'),
    path('import_csv/', views.import_csv, name='import_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)