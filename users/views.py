from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .forms import CustomUserForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("main:home")
        else:
            messages.error(request,'Invalid password or username')
            return render(request, 'users/login.html')
    return render(request,'users/login.html')

def register(request):
    if request.method == "GET":
        form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('main:home')
    context = {"form": form}
    return render(request, 'users/register.html',context)

