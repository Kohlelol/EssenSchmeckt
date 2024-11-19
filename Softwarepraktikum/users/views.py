from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here

def users_view(request):
    return redirect('users:login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('users:redirect')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required(login_url='/users/login/')
def redirect_view(request):
    user = request.user
    if user.groups.filter(name='admin').exists():
        return redirect('')
    elif user.groups.filter(name='facility_manager').exists():
        return redirect('')
    elif user.groups.filter(name='groupleader').exists():
        return redirect('')
    elif user.groups.filter(name='kitchen_staff').exists():
        return redirect('')