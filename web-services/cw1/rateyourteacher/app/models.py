from django.db import models


"""TODO str dunder methods"""
# Create your models here.
class Professor(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.code})"
        
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.email})"
    

class Module(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class ModuleInstance(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.module} ({self.year}, Semester {self.semester})"
    

class ProfessorModule(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.professor} teaching module instance [{self.module_instance}]"

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor_module = models.ForeignKey(ProfessorModule, on_delete=models.CASCADE)
    rating = models.FloatField() # Back-end validation for vote range

    """Cannot have duplicate entry"""

    def __str__(self):
        return f"{self.user} gave {self.rating} stars to {self.professor_module}]"
