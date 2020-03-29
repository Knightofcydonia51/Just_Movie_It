from django.contrib import admin
from django.urls import path, include
from movies import views as movie_views

urlpatterns = [
    path('', movie_views.index),
    path('admin/', admin.site.urls),
    path('movie_master/', include('movie_master.urls')),
    path('movies/', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
]