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
    DATA_TYPE_CHOICES = [
        ('int', 'Integer'),
        ('float', 'Float'),
        ('str', 'String'),
    ]
    INPUT_TYPE_CHOICES = [
        ('number', 'Number'),
        ('text', 'String'),
        ('select', 'DropDown'),
        ('radio', "Radio buttons"),
        ('checkbox', 'Checkbox')
    ]
    name = models.CharField(max_length=50)
    dataType = models.CharField(max_length=50, choices= DATA_TYPE_CHOICES)
    inputType = models.CharField(max_length=50, choices= INPUT_TYPE_CHOICES)
    default_value = models.CharField(max_length=50, blank=True)
    min_value = models.CharField(max_length=50, null= True)
    max_value = models.CharField(max_length=50, null= True)
    oprID = models.ForeignKey(Operation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.oprID.name} {self.name}"
    
class Option(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    option_no = models.IntegerField()
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.parameter.name} {self.option_no}"