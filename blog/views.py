from io import IncrementalNewlineDecoder
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.shortcuts import render,HttpResponseRedirect

from blog.models import Post
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages

from blog import forms


# Home
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts': posts})

# About
def about(request):
    return render(request,'blog/about.html')

# contact 
def contact(request):
    return render(request,'blog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        fname=user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':fname,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

        

# signup
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You have become Authour')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()

    return render(request,'blog/signup.html',{'form':form})

# login
def user_login(request):
    if not request.user.is_authenticated :
        if request.method== "POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname,password = upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'logged in successfully !!')
                    return HttpResponseRedirect('/dashboard')
        else:
            form = LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

# Add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title= title,desc = desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


# Update post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi= Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title= title,desc = desc)
                pst.save()        
        else:
            pi= Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi= Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')