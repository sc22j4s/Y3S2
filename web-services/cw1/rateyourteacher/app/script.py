from django.db import models
from models import *

x = User.objects.all()[0]
x.username = "Iris_Wood"
x.email = "iwood@gmail.com"
x.password = "mewoemwoemoew"
x.save()
