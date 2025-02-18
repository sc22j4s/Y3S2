from django.db import models

# Create your models here.
class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    rating = models.FloatField()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Module(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)

class ModuleInstance(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()

class ProfessorModule(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)   

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor_module = models.ForeignKey(ProfessorModule, on_delete=models.CASCADE)
    rating = models.FloatField()
