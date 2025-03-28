from django.db import models
from django.db.models.signals import post_delete

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver




def generate_code(name, table):
    """
    Takes first (and second) capitalised words of name and concatenates them,
    Appends unique number to avoid duplicate instances. 
    Used for Module and Professor tables' primary key generation.

    Example for modules:
        [name] -> [code]
        Web Services and Web Data -> WS1
        Formal Methods -> FM1
        Web Security -> WS2

    Example for professors:
        [name] -> [code]
        John Doe -> JD1
        Jane Doe -> JD2
        John Smith -> JS1
    """
    capital_words = [w for w in name.split() if w and w[0].isupper()]   
    if len(capital_words) >= 2:
        letters = capital_words[0][0] + capital_words[1][0]

    elif len(capital_words) == 1:
        letters = capital_words[0][0]

    else: 
        # No capitalised words (error input - should be edited in admin site)
        letters = "!!"

    code = letters.upper()

    # Query table for similar codes
    i = 1
    while table.filter(code=f"{code}{str(i)}").exists():
        i += 1
    code = f"{code}{str(i)}"
    return code

class Module(models.Model):
    code = models.CharField(max_length=5, primary_key=True, editable=False) # Can't be defined on admin site
    name = models.CharField(max_length=100)
    
    # Generate unique primary key
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name, self.__class__.objects.all())
            
        super().save(*args, **kwargs)
            

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class ModuleInstance(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])

    # Can't allow same module taught at same time
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['module', 'year', 'semester'], name='unique_module_instance')
        ]


    def __str__(self):
        return f"{self.module} ({self.year}, Semester {self.semester})"
    

# Create your models here.
class Professor(models.Model):
    code = models.CharField(max_length=5, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], 
                               editable=True,
                               null=True,
                               default=None) # Back-end validation for vote range

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name, self.__class__.objects.all())

        if not self.name.startswith("Prof. "):
            self.name = "Prof. " + self.name

        super().save(*args, **kwargs)

    def update_rating(self):

        ratings = Rating.objects.filter(professor_module__professor=self)
        if ratings.exists():
            self.rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            super().save()
        else:
            self.rating = None
            super().save()

    def __str__(self):
        return f"{self.name} ({self.code})"

class ProfessorModule(models.Model):
    id = models.AutoField(primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)  

    # Can't have same professor on the same module instance
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['professor', 'module_instance'], name='unique_professor_module')
        ]

    def __str__(self):
        return f"{self.professor} teaching module instance [{self.module_instance}]"



class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor_module = models.ForeignKey(ProfessorModule, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # Back-end validation for vote range

    # Cannot have duplicate entry6
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'professor_module'], name='unique_rating')
        ]

    # Update professor rating after saving
    def save(self, *args, **kwargs):   
        super().save(*args, **kwargs)
        self.professor_module.professor.update_rating()
    
    def __str__(self):
        return f"{self.user} gave {self.rating} stars to {self.professor_module}]"

