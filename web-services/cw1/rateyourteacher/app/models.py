from django.db import models
from django.contrib.auth.models import User

def generate_code(name):
    """
    Takes first (and second) capitalised words of name and concatenates them,
    Appends unique number to avoid duplicate instances. 
    Used for Module and Professor tables' primary key generation.

    Example for modules:
        [name] -> [code]
        Web Services and Web Data -> WS1
        Formal Methods -> FM1
        Web Security -> WS2
    """
    
    capital_words = [w for w in name.split() if w and w[0].isupper()]   

    if len(capital_words) >= 2:
        letters = capital_words[0][0] + capital_words[1][0]
    elif len(capital_words) == 1:
        letters = capital_words[0][1]
    else:
        letters = "!!"

    # Check for preexisting codes in table
 
    
    

"""TODO str dunder methods"""
# Create your models here.
class Professor(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    rating = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name, self.__class__.objects.all())

            
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.code})"

class Module(models.Model):
    code = models.CharField(max_length=5, primary_key=True, editable=False) # Can't be defined on admin site
    name = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name)


            i = 1
            while True:
                if self.__class__.objects.filter(code=f"{self.code}{str(i)}").exists():
                    i += 1
                else:
                    self.code = f"{self.code}{str(i)}"
                    break

            # Query table for similar codes
            
        super().save(*args, **kwargs)
            

            

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
