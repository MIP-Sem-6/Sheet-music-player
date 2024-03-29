from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Song,Friend
from django.contrib.auth import logout
from django.contrib import messages
from users.models import Profile
from django.contrib.auth.models import User
import pdfkit
from django.template import loader
from PIL import Image
import io,cv2,numpy
from .tf_model import predictStrip
import ast,re
from django.core.mail import send_mail,EmailMessage






# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    trending_songs = Song.objects.all().order_by('-play_count')

    dance_songs = trending_songs.filter(tags__icontains='dance')
    happy_songs = trending_songs.filter(tags__icontains='happy')
    romantic_songs = trending_songs.filter(tags__icontains='romantic')
    rock_songs = trending_songs.filter(tags__icontains='rock')
    classical_songs = trending_songs.filter(tags__icontains='classical')
    sad_songs = trending_songs.filter(tags__icontains='sad')
    inspiration_songs = trending_songs.filter(tags__icontains='inspiration')

    f = Profile.objects.all()
    f = f.exclude(user=request.user)


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
        'dance_songs' : dance_songs,
        'happy_songs' : happy_songs,
    'romantic_songs' : romantic_songs,
    'rock_songs' : rock_songs,
    'classical_songs' : classical_songs,
    'sad_songs' : sad_songs,
    'inspiration_songs' : inspiration_songs,
    'f':f,
   
    }
    return render(request,'main/index.html',context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')
    songs = Song.objects.all()
    mysongs = songs.filter(user=request.user.id)
    favsongs = songs.filter(likedby=request.user)

    song_count = len(mysongs)
    fav_count = len(favsongs)

    f = Friend.objects.all()
    f = f.filter(user1=request.user)

    p = Profile.objects.get(user=request.user)
    my_tags = str(p.tags).split(' ')
    my_tags = [i for i in my_tags if i]

    fr = Friend.objects.all()
    fr2 = f.filter(user1=request.user)
    following = len(fr2)
    followers = 0
    for o in fr:
        if o.user2 == request.user:
            followers += 1

    if request.is_ajax():
        count =request.POST.get('count')
        sid =request.POST.get('id')
        if int(count) == 1:
            sid = int(sid)
            song = Song.objects.get(id=sid)
            song.play_count = 1 + song.play_count
            song.save()

    f2 = Friend.objects.all()
    f2 = f2.filter(user2=request.user)
    li = []
    for obj in f2:
        li.append(obj.user1.id)
    li = set(li)
    y = Profile.objects.all()
    li2 = []
    for t in y:
        if t.user.id in li:
            li2.append(t)



    context = {
        'my_songs' : mysongs,
        'profile':p,
        'count_my':song_count,
        'count_fav':fav_count,
        'f':f,
        'following':following,
        'followers':followers,
        'f2':li2,
        'my_tags':my_tags,
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

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    u = request.user
    p = Profile.objects.get(user=u)
    context = {
        'u':u,
        'p':p,
    }
    return render(request,'main/edit_profile.html',context)

def view_profile(request,id):
    if not request.user.is_authenticated:
        return redirect('errorpage')
    
    obj = User.objects.get(id=id)
    pro = Profile.objects.get(user=obj)
    my_tags = str(pro.tags).split(' ')
    my_tags = [i for i in my_tags if i]

    is_friend = False
    since = ''
    f = Friend.objects.all()
    f = f.filter(user1=request.user)
    for o in f:
        if o.user2 == obj:
            is_friend = True
            since = o.since
            break

    songs = Song.objects.all()
    mysongs = songs.filter(user=obj)
    favsongs = songs.filter(likedby=obj)

    song_count = len(mysongs)
    fav_count = len(favsongs)

    fr = Friend.objects.all()
    fr2 = fr.filter(user1=obj)
    following = len(fr2)
    followers = 0
    for o in fr:
        if o.user2 == obj:
            followers += 1

    if 'unfollow' in request.POST:
        f = Friend.objects.all()
        f1 = f.filter(user1 = request.user,user2=obj)
        f1.delete()
        messages.success(request,f'You have unfollowed {obj}!')
        return redirect('view_profile',id)

    if 'follow' in request.POST:
        Friend.objects.create(user1=request.user,user2=obj,profile2=pro)
        messages.success(request,f'You followed {obj}!')
        return redirect('view_profile',id)


    context = {
        'obj' : obj,
        'profile' : pro,
        'is_friend':is_friend,
        'since':since,
        'mysongs':mysongs,
        'count_my':song_count,
        'count_fav':fav_count,
        'following':following,
        'followers':followers,
        'my_tags':my_tags,
    }   
    
    return render(request,'main/view_profile.html',context)

def tag(request,name):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    my_songs = Song.objects.all()
    my_songs = my_songs.filter(tags__icontains=name)

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
        'name':name,
    }
    return render(request,'main/tag.html',context)

def get_notes(x):
    res = x.strip()
    s = ''
    li = []
    for y in res:
        if y==" ":
            continue
        elif y ==']':
            s += y
            li.append(s)
            s = ''
        else:
            s += y
    fin = []
    for x in li:
        fin.append(ast.literal_eval(x))
    return fin

def audio(request,id):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    
    tab = 0
    mynotes = ''

    if 'image' in request.POST:
        img = cv2.imdecode(numpy.fromstring(request.FILES['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        readable = predictStrip.imageToNotes(img)
        mynotes = readable
        id = 2

    if 'pdf' in request.POST:
        notes = request.POST.get("notes")
        template = loader.get_template('main/notes.html')
        html = template.render({'notes':notes,'user':request.user})
        options = {
        'page-size':'Letter',
        'encoding':"UTF-8",
        }
        pdf = pdfkit.from_string(html,False,options)
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment'
        return response

    if 'audio' in request.POST:
        val = request.POST.get("notes")
        val = get_notes(val)
        print(val)
        #notes = [['clef-G2', 'timeSignature-6/4', 'note-E4_quarter', 'note-D4_quarter', 'note-F4_quarter', 'note-G4_quarter', 'barline', 'note-G4_quarter', 'note-F4_half', 'note-D4_quarter', 'note-D4_quarter', 'barline', 'note-C4_quarter', 'note-C4_half', 'note-D4_quarter', 'note-D4_quarter', 'barline', 'note-D4_quarter.', 'note-D4_quarter', 'note-D4_half.', 'barline'], ['clef-G2', 'timeSignature-C/', 'note-D4_quarter', 'note-F4_quarter', 'note-E4_quarter', 'barline', 'note-F4_quarter', 'note-F4_half', 'note-D4_quarter', 'note-D4_quarter', 'barline', 'note-C4_half', 'note-C4_quarter', 'note-D4_quarter', 'note-D4_quarter', 'barline', 'note-B3_quarter', 'barline'], ['clef-G2', 'timeSignature-3/2', 'note-D4_quarter', 'note-D4_quarter', 'note-D4_quarter', 'note-B3_quarter', 'barline', 'note-D4_quarter', 'note-D4_quarter', 'note-D4_quarter', 'note-D4_quarter', 'note-C4_quarter', 'barline', 'note-D4_quarter', 'note-D4_quarter', 'note-F4_quarter', 'note-E4_quarter', 'note-C4_quarter', 'barline', 'note-C4_half', 'note-D4_quarter', 'note-C5_half', 'note-D4_quarter', 'barline'], ['clef-G2', 'timeSignature-6/8', 'note-D4_quarter', 'note-C4_quarter', 'note-D4_quarter', 'note-F4_eighth', 'barline', 'note-D4_quarter', 'note-D4_eighth', 'note-D4_quarter', 'note-B3_eighth', 'barline', 'note-B3_sixteenth', 'note-A3_sixteenth', 'note-B3_eighth', 'note-C4_eighth', 'barline', 'note-B3_sixteenth', 'note-B3_sixteenth', 'barline']]
        predictStrip.notesToMusic(val)
        print("Music banaya badaa mazaa aaya")
        messages.success(request,f'Audio file generated successfully!')
        tab = 1
        id = 2
        #call function to generate audio file

    if 'send_email' in request.POST:
        email = request.POST.get("email")
        email = re.sub('\s+',' ',email)
        val = request.POST.get("notes")
        subject = f'Notes by {request.user.username}'
        message = re.sub('\s+',' ',val)
        val = get_notes(val)
        email_from = 'himali.saini@somaiya.edu'
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request, 'Email has been sent')
        id = 2
        mynotes = val
    
    if 'send_audio' in request.POST:
        email = request.POST.get("email_audio")
        email = re.sub('\s+',' ',email)
        subject = f'Audio file by {request.user.username}'
        message = f'Service provided by SMP'
        mail = EmailMessage(subject, message, 'smp.mip123@gmail.com', [email])
        mail.attach_file('/home/boomerang/boomerang/BTech_CS/MIP-Sem6/cloned/Sheet-music-player/app/main/static/main/music/music-file.mp3')
        mail.send()
        messages.success(request, 'Email has been sent')
        id = 2
        tab = 1
        print('hiiii')
        
    
    context = {
        'id':id,
        'tab':tab,
        'path': 'main/music/music-file.mp3',
        'readable':mynotes,
    }

    return render(request,'main/audio.html',context)

def download(request,notes):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    template = loader.get_template('main/notes.html')
    html = template.render({'notes':notes,'user':request.user})
    options = {
        'page-size':'Letter',
        'encoding':"UTF-8",
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    return response



