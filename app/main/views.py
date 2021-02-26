from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Song
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
        if(fav_song):
            fs = Song.objects.get(id=int(fav_song))
            fs.likedby.add(request.user)

        remove_song = request.POST.get('remove_fav')
        if(remove_song):
            rs = Song.objects.get(id=int(remove_song))
            rs.likedby.remove(request.user)

    for x in trending_songs:
        print(x.get_is_liked(request.user))


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

def fav(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    my_songs = Song.objects.all()
    my_songs = my_songs.filter(likedby=request.user)

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


def add_song_form(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    if request.method == 'POST':
        filename =request.FILES['file']
        title =request.POST.get("title")
        album =request.POST.get("album")
        img =request.FILES["image"]
        tags =request.POST.get("tags")
        u = request.user

        Song.objects.create(file=filename,title=title,album=album,user=u,tags=tags,cover_image=img).save()



    return render(request,'main/_song_form.html')

def update_song_form(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    if request.method == 'POST':
        filename =request.FILES['file']
        title =request.POST.get("title")
        album =request.POST.get("album")
        img =request.FILES["image"]
        tags =request.POST.get("tags")
        u = request.user

        Song.objects.create(file=filename,title=title,album=album,user=u,tags=tags,cover_image=img).save()



    return render(request,'main/update_song_form.html')