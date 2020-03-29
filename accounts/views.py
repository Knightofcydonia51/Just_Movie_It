from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Movie, Genre, Review
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from movies.models import Movie, Genre, Review
from .forms import CustomUserCreationForm, CustomUserChangeForm
from IPython import embed



def index(request):
    if not request.user.is_authenticated:
        return redirect('movies:index')
    users = get_user_model().objects.all().order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'accounts/index.html', context)
    

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:recommend')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/forms.html', context)


def logout(request):
    auth_logout(request)
    return redirect('movies:index')


def detail(request, user_id):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)
    user = get_object_or_404(get_user_model(), id=user_id)

    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)


def update(request, user_id):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=user)
    context = {'form': form,}
    # embed()
    return render(request, 'accounts/forms.html', context)


def delete(request, user_id):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)
    user = get_object_or_404(get_user_model(), id=user_id)
    user.delete()
    return redirect('accounts:index')


def follow(request, user_id):
    if request.is_ajax():
        # embed()

        # 게시글을 작성한 유저
        person = get_object_or_404(get_user_model(), pk=user_id)
        # 해당 경로로 요청을 보낸 사람
        user = request.user

        # 해당 person의 팔로워 중에서 요청을 보낸 사람이 존재 하면 언팔로우
        if person.followers.filter(pk=user.pk):
            person.followers.remove(user)
            
            followed = False
        else:
            person.followers.add(user)
            followed = True
        context = {
            'followed': followed,
            'count': user.followers.count(),
        }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


def profile(request, user_id):
    profile_user = get_object_or_404(get_user_model(), id=user_id)
    like_movies = profile_user.like_movies.all()[:4]
    followers = profile_user.followers.all()[:5]
    follows = profile_user.followings.all()[:5]
    reviews = profile_user.reviews.all()[:5]
    context = {
        'profile_user': profile_user,
        'like_movies': like_movies,
        'followers': followers,
        'follows': follows,
        'reviews': reviews,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def update_profile(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.user == user:
        user.profile = request.POST.get('profile')
        user.save()
    else:
        return HttpResponse('401 Unauthorized Access', status=401)
    return redirect('accounts:profile', user_id)


def followers(request, user_id):
    profile_user = get_object_or_404(get_user_model(), id=user_id)
    followers = profile_user.followers.all()
    context = {
        'profile_user': profile_user,
        'followers': followers,
    }
    return render(request, 'accounts/followers.html', context)
    

def follows(request, user_id):
    profile_user = get_object_or_404(get_user_model(), id=user_id)
    follows = profile_user.followings.all()
    context = {
        'profile_user': profile_user,
        'follows': follows,
    }
    return render(request, 'accounts/follows.html', context)


def like_movies(request, user_id):
    profile_user = get_object_or_404(get_user_model(), id=user_id)
    like_movies = profile_user.like_movies.all()
    context = {
        'profile_user': profile_user,
        'like_movies': like_movies,
    }
    return render(request, 'accounts/like_movies.html', context)


def reviews(request, user_id):
    reviews = Review.objects.filter(user_id=user_id)
    profile_user = get_object_or_404(get_user_model(), id=user_id)
    context = {
        'reviews': reviews,
        'profile_user': profile_user
    }
    return render(request, 'accounts/reviews.html', context)