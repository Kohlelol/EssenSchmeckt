from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'users'

urlpatterns = [
    path('', views.users_view, name="users"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('select/', views.select_view, name="select"),
]