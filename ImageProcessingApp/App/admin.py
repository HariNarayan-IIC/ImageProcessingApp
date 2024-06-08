from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(History)
admin.site.register(Attribute)
admin.site.register(Category)
admin.site.register(Operation)
admin.site.register(Parameter)