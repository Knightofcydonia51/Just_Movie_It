from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('master_index/', views.master_index, name='master_index'),
    path('getdata/', views.getdata, name='getdata'),
    path('detail/<int:movie_id>/', views.detail, name='detail'),
    path('like/<int:movie_id>/', views.like, name='like'),
    path('<int:movie_id>/reviews/new/', views.review_create, name='review_create'),
    path('<int:movie_id>/reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_id>/reviews/<int:review_id>/update/', views.review_update, name='review_update'),
    path('update/<int:movie_id>/', views.update, name='update'),
    path('delete/<int:movie_id>/', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('recommend/', views.recommend, name='recommend'),
    path('search/', views.search, name='search'),
    path('more_recommend/<int:user_id>/', views.more_recommend, name='more_recommend'),
]
