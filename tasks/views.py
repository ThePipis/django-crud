from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
# Create your views here.


def home(request):
    return render(request, "home.html")


def sigunp(request):
    if request.method == 'GET':
        return render(request, 'sigunp.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'sigunp.html', {
                    'form': UserCreationForm,
                    'error': 'usuario ya existe'
                })

        return render(request, 'sigunp.html', {
            'form': UserCreationForm,
            'error': "Las passwords no coinciden."
        })

@login_required
def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'usuario o pass incorrecto'
            })
        else:
            login(request, user)
            return redirect('tasks')
