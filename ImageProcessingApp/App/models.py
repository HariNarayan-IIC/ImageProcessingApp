from django.db import models

# Create your models here.
class History(models.Model):
    operation = models.CharField(max_length= 30)

class Attribute(models.Model):
    name= models.CharField(max_length= 30)
    value= models.CharField(max_length= 30)
    history= models.ForeignKey(History, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Operation(models.Model):
    name = models.CharField(max_length=50)
    catID = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=50)
    valueType = models.CharField(max_length=50)
    default_value = models.CharField(max_length=50, blank=True)
    oprID = models.ForeignKey(Operation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
