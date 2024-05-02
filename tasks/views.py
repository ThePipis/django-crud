from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm, ProgramaForm
from .models import Task, Programa
from django.utils import timezone
from django.http import HttpRequest
# Create your views here.
import subprocess
import os
import json


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
    tasks = Task.objects.filter(user=request.user, datacompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datacompleted__isnull=False).order_by('-datacompleted')
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor ingresa datos validos.'
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error actualizando updating task.'
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datacompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


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


@login_required
def listar_programas(request: HttpRequest):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        servers = request.POST.get('servername')

        # Procesar la entrada de servidores: dividir por líneas, limpiar espacios, y eliminar líneas vacías
        servers_list = [server.strip()
                        for server in servers.splitlines() if server.strip()]
        # Formatea como array de PowerShell
        servers_formatted = '@("' + '","'.join(servers_list) + '")'
        print(servers_formatted)
        script_path = os.path.join(
            os.path.dirname(__file__), 'templates', 'scripts', 'listar-programas.ps1')
        ps_command = f"& '{script_path}' -ComputerName {servers_formatted} -Username '{usuario}' -Password '{password}'"

        try:
            output = subprocess.run(
                ["powershell", "-Command", ps_command], capture_output=True, text=True, timeout=60)
            print("Raw output:", output.stdout)
            # Intenta cargar el JSON de la salida estándar
            data = json.loads(output.stdout if output.stdout else '[]')
            # print(type(data))
            print("JSON Data:", data)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            data = []
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el script de PowerShell: {e.output}")
            data = []
        except FileNotFoundError:
            print("Script file not found.")
            data = []
        except subprocess.TimeoutExpired as e:
            print(
                f"El script de PowerShell excedió el tiempo de espera: {str(e)}")
            data = []

        return render(request, 'programas.html', {
            # Asegúrate de que ProgramaForm está correctamente importado o definido
            'form': ProgramaForm(),
            'data': data,
            'server': servers  # Pasar la lista original o la formateada a la plantilla, según necesites
        })

    # Si no es POST, mostrar solo el formulario
    return render(request, 'programas.html', {
        'form': ProgramaForm()
    })
