from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainView, name= "home"),
    path("upload/", views.upload, name= "upload"),
    path("apply/",  views.apply , name="apply"),
    path("delete/<int:history_id>/", views.delete, name="delete"),
    path("update/", views.update, name= "update"),
    path("reset/", views.reset, name="reset"),
    path("download/", views.download, name="download"),
    path('ajax/load-operations/', views.load_operations, name='ajax_load_operations'),
    path('ajax/load-parameters/', views.load_parameters, name='ajax_load_parameters'),
    path('ajax/load-options/', views.load_options, name= 'ajax_load_options'),
    path('fetch-parameters/', views.fetch_parameters, name='fetch_parameters'),
    path('fetch-options/', views.fetch_options, name = "fetch_options"),
    path('update-parameters/', views.update_parameters, name='update_parameters'),
]