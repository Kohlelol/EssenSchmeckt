from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'database'

urlpatterns = [
    path('', views.database_list, name='database_list'),
    path('attendance/', views.attendance, name='attendance'),
    path('daily_order/', views.daily_order, name='daily_order'),
    path('edit_orders/', views.edit_orders, name='edit_orders'),
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)