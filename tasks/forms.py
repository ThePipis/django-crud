from django.forms import ModelForm
from .models import Task, Programa


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']


class ProgramaForm(ModelForm):
    class Meta:
        model = Programa
        fields = ['servername']
