from django.urls import path
from . import views
from django.views.generic import TemplateView

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
]