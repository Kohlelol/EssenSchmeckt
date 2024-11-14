# from django.http import HttpResponse
from django.shortcuts import render


def login(request):
    return render(request, 'login.html')

def homepage(request):
    return render(request, 'home.html')