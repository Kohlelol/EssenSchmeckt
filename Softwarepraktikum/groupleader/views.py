from django.shortcuts import render

# Create your views here.

def groupmember_list(request):
    return render(request, 'groupleader/groupmember_list.html')
