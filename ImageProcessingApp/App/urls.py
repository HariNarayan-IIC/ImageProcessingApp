from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainView, name= "home"),
    path("upload/", views.upload, name= "upload"),
    path("apply/",  views.apply , name="apply"),
    path("delete/<int:history_id>/", views.delete, name="delete"),
    path("update/<int:history_id>/", views.update, name= "update"),
    path("reset/", views.reset, name="reset"),
    path("download/", views.download, name="download"),
    path('ajax/load-operations/', views.load_operations, name='ajax_load_operations'),
    path('ajax/load-parameters/', views.load_parameters, name='ajax_load_parameters'),
    path('fetch-parameters/', views.fetch_parameters, name='fetch_parameters'),
    path('update-parameters/', views.update_parameters, name='update_parameters'),
]