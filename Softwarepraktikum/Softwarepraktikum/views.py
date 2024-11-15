# from django.http import HttpResponse
from django.shortcuts import render, redirect



def login(request):
    return render(request, 'login.html')

def homepage(request):
    return redirect('users:login')
    # return render(request, 'home.html')