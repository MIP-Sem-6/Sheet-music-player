from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Song
from django.contrib.auth import logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    my_songs = Song.objects.all()
    my_songs = my_songs.filter(user=request.user.id)

    context = {
        'my_songs' : my_songs,
    }
    return render(request,'main/home.html',context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')
    return render(request,'main/profile.html')

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    logout(request)
    return redirect('signin') 
