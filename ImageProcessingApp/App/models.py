from django.db import models

# Create your models here.
class History(models.Model):
    operation = models.CharField(max_length= 30)

class Attributes(models.Model):
    name= models.CharField(max_length= 30)
    value= models.CharField(max_length= 30)
    history= models.ForeignKey(History, on_delete=models.CASCADE)
