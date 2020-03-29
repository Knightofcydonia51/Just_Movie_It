from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('detail/<int:user_id>', views.detail, name='detail'),
    path('update/<int:user_id>', views.update, name='update'),
    path('delete/<int:user_id>', views.delete, name='delete'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('update_profile/<int:user_id>/', views.update_profile, name='update_profile'),    
    path('like_movies/<int:user_id>/', views.like_movies, name='like_movies'),
    path('follows/<int:user_id>/', views.follows, name='follows'),
    path('followers/<int:user_id>/', views.followers, name='followers'),
    path('reviews/<int:user_id>/', views.reviews, name='reviews'),
]
