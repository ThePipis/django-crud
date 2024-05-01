from django.contrib import admin
from .models import Task,Programa

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["created",]

class ProgramaAdmin(admin.ModelAdmin):
    readonly_fields = ["upload",]
# Register your models here.
admin.site.register(Task,TaskAdmin)
admin.site.register(Programa,ProgramaAdmin)