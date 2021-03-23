from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Song
from django.contrib.auth import logout
from django.contrib import messages


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

    if 'subscribe' in request.POST:
        fav_song = request.POST.get('songid')
        fs = Song.objects.get(id=fav_song)
        fs.likedby.add(request.user)
        messages.success(request,f'Added to favourites!')
        print(f'{request.user} liked {fs.title}')
        return redirect('index')
    
    if 'unsubscribe' in request.POST:
        fav_song = request.POST.get('songid')
        fs = Song.objects.get(id=fav_song)
        fs.likedby.remove(request.user)
        messages.success(request,f'Removed from favourites!')
        print(f'{request.user} unliked {fs.title}')
        return redirect('index')

    if 'delete' in request.POST:
        del_id = request.POST.get('songid_delete')
        fs = Song.objects.get(id=del_id)
        fs.delete()
        messages.success(request,f'Song has been deleted!')
        return redirect('index')

    context = {
        'my_songs' : trending_songs,
    }
    return render(request,'main/index.html',context)

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
    return render(request,'main/account.html',context)

def fav(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    my_songs = Song.objects.all()
    my_songs = my_songs.filter(likedby=request.user)

    if 'subscribe' in request.POST:
        fav_song = request.POST.get('songid')
        fs = Song.objects.get(id=fav_song)
        fs.likedby.add(request.user)
        messages.success(request,f'Added to favourites!')
        print(f'{request.user} liked {fs.title}')
        return redirect('index')
    
    if 'unsubscribe' in request.POST:
        fav_song = request.POST.get('songid')
        fs = Song.objects.get(id=fav_song)
        fs.likedby.remove(request.user)
        messages.success(request,f'Removed from favourites!')
        print(f'{request.user} unliked {fs.title}')
        return redirect('index')


    context = {
        'my_songs' : my_songs,
    }
    return render(request,'main/fav.html',context)

def my_songs(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    my_songs = Song.objects.all()
    my_songs = my_songs.filter(user=request.user)

    if 'subscribe' in request.POST:
        fav_song = request.POST.get('songid')
        fs = Song.objects.get(id=fav_song)
        fs.likedby.add(request.user)
        messages.success(request,f'Added to favourites!')
        print(f'{request.user} liked {fs.title}')
        return redirect('index')
    
    if 'unsubscribe' in request.POST:
        fav_song = request.POST.get('songid')
        fs = Song.objects.get(id=fav_song)
        fs.likedby.remove(request.user)
        messages.success(request,f'Removed from favourites!')
        print(f'{request.user} unliked {fs.title}')
        return redirect('index')


    context = {
        'my_songs' : my_songs,
    }
    return render(request,'main/my_songs.html',context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    logout(request)
    return redirect('signin') 


def add_song(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    if request.method == 'POST':
        st = ''
        filename =request.FILES['file']
        title =request.POST.get("title")
        album =request.POST.get("album")
        rock =request.POST.get("rock")
        artist =  request.POST.get("artist")
        if(rock):
            st += rock + ' '
        inspiration =request.POST.get("inspiration")
        if(inspiration):
            st += inspiration + ' '
        dance =request.POST.get("dance")
        if(dance):
            st += dance + ' '
        happy =request.POST.get("happy")
        if(happy):
            st += happy + ' '
        sad =request.POST.get("sad")
        if(sad):
            st += sad + ' '
        classical =request.POST.get("classical")
        if(classical):
            st += classical + ' '
        romantic =request.POST.get("romantic")
        if(romantic):
            st += romantic + ' '
        
        print(st)
        u = request.user
        try:
            img =request.FILES["image"]
            if(img):
                Song.objects.create(file_name=filename,artist=artist,title=title,album=album,user=u,tags=st,cover_image=img).save()
                messages.success(request,f'Song added successfully!')
                return redirect('index')
        except:
            pass

        Song.objects.create(file_name=filename,artist=artist,title=title,album=album,user=u,tags=st).save()
        messages.success(request,f'Song added successfully!')
        return redirect('index')



    return render(request,'main/add_song.html')

# def update_song_form(request,id):
#     if not request.user.is_authenticated:
#         return redirect('errorpage')

#     getSong = Song.objects.get(id=id)

#     if request.method == 'POST':
#         title =request.POST.get("title")
#         album =request.POST.get("album")
#         tags =request.POST.get("tags")
#         u = request.user
#         try:
#             filename =request.FILES['file']
#             getSong.file = filename
#         except:
#             pass
#         try:
#             img =request.FILES["image"]
#             getSong.cover_image = img
#         except:
#             pass

#         getSong.title = title
#         getSong.album = album
#         getSong.tags = tags
#         getSong.save()

#         return redirect('index')

#     context = {
#         'song' : getSong,
#     }

#     return render(request,'main/update_song_form.html',context)

def update_song(request,id):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    getSong = Song.objects.get(id=id)

    context = {
        'song' : getSong,
    }
    return render(request,'main/update_song.html',context)


