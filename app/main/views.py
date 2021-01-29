from django.shortcuts import render,redirect
from django.http import HttpResponse


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('error_page')
    return HttpResponse("Welcome to the home page.Waiting for template....")
