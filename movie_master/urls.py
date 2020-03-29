from django.urls import path
from . import views

app_name='movie_master'

urlpatterns = [
    path('', views.index, name='index'),
    path('getdata', views.getdata, name='getdata'),
]
