from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Song, FavouriteSong
from django.contrib.auth import logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    trending_songs = Song.objects.all().order_by('-play_count')

    if request.is_ajax():
        count =request.POST.get('count')
        sid =request.POST.get('id')
        if count:
            sid = int(sid)
            song = Song.objects.get(id=sid)
            song.play_count = 1 + song.play_count
            song.save()
        
        fav_song = request.POST.get('add_fav')
        print(fav_song)
        if(fav_song):
            fs = Song.objects.get(id=int(fav_song))
            FavouriteSong(user=request.user,song=fs).save()


    context = {
        'my_songs' : trending_songs,
    }
    return render(request,'main/home.html',context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')
    my_songs = Song.objects.all()
    my_songs = my_songs.filter(user=request.user.id)

    if request.is_ajax():
        count =request.POST.get('count')
        sid =request.POST.get('id')
        if int(count) == 1:
            sid = int(sid)
            song = Song.objects.get(id=sid)
            song.play_count = 1 + song.play_count
            song.save()

    context = {
        'my_songs' : my_songs,
    }
    return render(request,'main/profile.html',context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    logout(request)
    return redirect('signin') 
