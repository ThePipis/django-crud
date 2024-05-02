from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datacompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return 'Tarea: '+self.title+' - '+'Usuario: '+self.user.username


class Programa(models.Model):
    servername = models.TextField(null=False, blank=False)
    upload = models.DateTimeField(auto_now_add=True)
    displayname = models.CharField(max_length=500)
    displayversion = models.CharField(max_length=500)
    installdate = models.DateTimeField(null=True, blank=True)
    installedfor = models.CharField(max_length=200)
    installlocation = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
        ordering = ['-installdate']

    def __str__(self) -> str:
        return 'Programa: ' + self.displayname + ' - ' + 'Instalado por: ' + self.installedfor
