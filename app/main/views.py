from django.shortcuts import render,redirect
from django.http import HttpResponse


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')
    return render(request,'main/home.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')
    return render(request,'main/profile.html')
