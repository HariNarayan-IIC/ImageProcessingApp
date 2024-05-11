from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainView, name= "home"),
    path("upload/", views.upload, name= "upload"),
    path("apply/",  views.apply , name="apply"),
    path("delete/<int:history_id>/", views.delete, name="delete"),
    path("update/<int:history_id>/", views.update, name= "update"),
    path("reset/", views.reset, name="reset")
]