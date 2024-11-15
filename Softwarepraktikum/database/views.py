from django.shortcuts import render

# Create your views here.

def groupmember_list(request):
    return render(request, 'database/database_list.html')
