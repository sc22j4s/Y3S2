from django.contrib import admin

from .models import Professor, Module, Student

# Register your models here.

admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Student)


