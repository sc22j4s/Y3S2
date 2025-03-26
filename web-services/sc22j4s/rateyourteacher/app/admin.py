from django.contrib import admin

from .models import Professor, Module, User, ModuleInstance, ProfessorModule, Rating

# Register your models here.
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Rating)
admin.site.register(ModuleInstance)
admin.site.register(ProfessorModule)

