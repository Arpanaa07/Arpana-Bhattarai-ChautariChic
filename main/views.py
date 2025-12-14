from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is the main app!")
    
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')
# Create your views here.
