from django.urls import path

from . import views

app_name = "brain"

urlpatterns = [
    path('', views.index, name='index'),
]
