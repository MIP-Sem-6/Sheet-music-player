from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Profile




# Create your views here.
def signin(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username=request.POST.get("username")
        psw =request.POST.get("pass")
        user = authenticate(request, username=username, password=psw)
        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            e = "Invalid username/password."
            return render(request,'users/login.html',{'e':e})

    return render(request,'users/login.html')


#Sign up 
def register(request,id,tab):
    if request.user.is_authenticated:
        return redirect('index')
        
    page = 1
    uname = ''
    if tab==2:
        page = 2

    if id!=0:
        us = User.objects.get(id=id)
        if uname:
            uname = us.username

    if 'next' in request.POST:
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        psw =request.POST.get("pass")
        
        try:

            u = User.objects.create_user(email=email,password=psw,username=username)
            u.first_name = fname
            u.last_name = lname
            u.save()
            messages.success(request,f'You have successfully registered!')
            user = authenticate(request, username=username, password=psw)
            if user is not None:
                login(request, user)
            Profile.objects.create(user=request.user)
            return redirect('complete')
        
        except:
            e='This username is already in use.Try again with a new one.'
            return render(request,'users/register.html',{'page':page,'e':e})

    print(request.user)
    return render(request,'users/register.html',{'page':page,'uname':uname})

def complete(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')
        
    page = 1
    uname = ''

    if 'submit' in request.POST:
        bio=request.POST.get("bio")
        pic =request.FILES['image']
        st = ''
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
        

        p = Profile.objects.get(user=request.user)
        p.bio = bio
        p.pic = pic
        p.tags = st
        p.save()
        messages.success(request,f'You have finished registration!')

        return redirect('index')
        
        '''except:
            e='Some error occured.Pls contact @MIP'
            return render(request,'users/complete.html',{'page':page,'e':e})'''

    print(request.user)
    return render(request,'users/complete.html',{'page':page})


def errorpage(request):
    return render(request,'users/errorpage.html')