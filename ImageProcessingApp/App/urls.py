from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainView, name= "home"),
    path("upload/", views.upload, name= "upload"),
    path("apply/", views.apply , name="apply"),
]