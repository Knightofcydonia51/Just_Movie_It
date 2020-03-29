from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Movie, Review, Genre
from .forms import ReviewForm, MovieForm
from decouple import config
import requests
import json
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from IPython import embed


def index(request):
    if request.user.is_authenticated:
        movies=Movie.objects.filter(age__lte=request.user.age)
        if request.user.is_authenticated:
            like_movies = request.user.like_movies.all()
        else:
            like_movies = []
        genres = Genre.objects.all()
        genrelist = [0 for _ in range(len(genres)+1)]
        for movie in like_movies:
            moviegenres = movie.genres.all()
            for genre in moviegenres:
                genrelist[genre.id] += 3
        reviews = request.user.reviews.all()
        for review in reviews:
            moviegenres = review.movie.genres.all()
            genre_score = review.score
            for genre in moviegenres:
                genrelist[genre.id] += genre_score
        
        idx = 1
        maxcnt = 0
        for i in range(len(genres)):
            if genrelist[i] > maxcnt:
                maxcnt = genrelist[i]
                idx = i



        like_genre = genres.get(id=idx)
        like_genre_movie = like_genre.movies.filter(age__lte=request.user.age).order_by('-audience')[0]
        idx = 0
        maxcnt = 0
        context={
            'like_genre': like_genre,
            'movies': movies,
            'like_genre_movie': like_genre_movie
            }
    else:
        context = {}
        
    return render(request, 'movies/index.html', context)



def master_index(request):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)
    movies = Movie.objects.all().order_by('-id')
    context = {
        'movies': movies,
    }
    
    return render(request, 'movies/master_index.html', context)


def detail(request, movie_id):
    movie=get_object_or_404(Movie, id=movie_id)
    reviews=movie.review_set.all()
    if reviews.filter(user=request.user):
        writed = True
    else:
        writed = False
    review_form=ReviewForm()
    context={
        'movie' : movie,
        'review_form' : review_form,
        'reviews' : reviews,
        'writed': writed,
    }
    return render(request, 'movies/detail.html', context)


@login_required
def like(request, movie_id):
    if request.is_ajax():
        movie = get_object_or_404(Movie, id=movie_id)
        user = request.user
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
        count = movie.like_users.count()
        if count:
            if count > 1:
                text = '{}외 {}명이 이 영화를 좋아합니다.'.format(movie.like_users.all()[0], count-1)
            else:
                text = '{}님이 이 영화를 좋아합니다.'.format(movie.like_users.all()[0])
        else:
            text = '현재 이 영화를 좋아하는 사람이 없습니다.'
        context = {
            'liked': liked,
            'text': text,
        }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


@require_POST
def review_create(request, movie_id):
    if request.user.is_authenticated:
        review_form=ReviewForm(request.POST)
        if review_form.is_valid():
            review=review_form.save(commit=False)
            review.movie_id=movie_id
            review.user=request.user
            review.save()
            return redirect('movies:detail', movie_id)
        else:
            return redirect('movies:detail', movie_id)


@require_POST     
def review_delete(request, movie_id, review_id):
    if request.user.is_authenticated:
        review=get_object_or_404(Review, id=review_id)
        if request.user==review.user:
            review.delete()
    return redirect('movies:detail', movie_id)


@require_POST
def review_update(request, movie_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)
        review_user = review.user
        if request.user == review_user:
            review_form=ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review=review_form.save(commit=False)
                review.movie_id=movie_id
                review.user=request.user
                review.save()
                return redirect('movies:detail', movie_id)
    return redirect('movies:detail', movie_id)

    
def getdata(request):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)
    key=config('API_KEY')
    NAVER_CLIENT_ID=config('NAVER_CLIENT_ID')
    NAVER_CLIENT_SECRET=config('NAVER_CLIENT_SECRET')

    headers = {
        'X-Naver-Client-Id' : NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
    }

    dateFrom=request.POST.get('dateFrom')
    dateTo=request.POST.get('dateTo')
    dateFrom = datetime(int(dateFrom[:4]),int(dateFrom[4:6]),int(dateFrom[6:]))
    dateTo = datetime(int(dateTo[:4]),int(dateTo[4:6]),int(dateTo[6:]))
    period=((dateTo-dateFrom).days)//7

    # 주간으로 바꾸고, 시작날짜, 끝나는날짜 입력받기, 관객 최신화

    for week in range(period):
        targetDt=dateTo-timedelta(weeks=week)
        targetDt=targetDt.strftime('%Y%m%d')
        movielist='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={}&targetDt={}&weekGb=0'.format(key,targetDt)
        response = requests.get(url=movielist)
        info = response.json()
        print(targetDt)
        print('start===============================')
        for i in info.get('boxOfficeResult').get('weeklyBoxOfficeList'):
            # t_time = now - datetime.timedelta(weeks=i)
            # t_time=t_time.strftime('%Y%m%d')
            title,director,grade,audi="","","",0
            movieGenre=[]
            # for k,v in i.items():  영화이름, 코드, 관객수 뽑아오기
            if i.get('movieNm'):
                nm=i.get('movieNm')
                validate = Movie.objects.filter(title=nm)
                if validate:
                    continue 
                else:
                    title=nm
            if i.get('movieCd'):
                v=i.get('movieCd')
                code=v  
                movieDetail='http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={}&movieCd={}'.format(key,code)
                detailResponse=requests.get(url=movieDetail)
                detailInfo=detailResponse.json().get('movieInfoResult').get('movieInfo')
                if detailInfo.get('audits'):
                    grade=detailInfo.get('audits')[0].get('watchGradeNm')
                    if grade:
                        if grade=="청소년관람불가":
                            grade=19
                        elif grade=="15세이상관람가":
                            grade=15
                        elif grade=="12세관람가":
                            grade=12
                        elif grade=="12세이상관람가":
                            grade=12
                        elif grade=="전체관람가":
                            grade=0
                        else:
                            grade=0
                    else: 
                        grade=99
                else:
                    grade=0
                if detailInfo.get('genres'):
                    for g in range(len(detailInfo.get('genres'))):
                        # print(len(detailInfo.get('genres')))
                        movieGenre.append(detailInfo.get('genres')[g].get('genreNm')) #장르 제대로 들어가고 있는지 확인
                if detailInfo.get('prdtYear'):
                    prdtYear=detailInfo.get('prdtYear')
                if detailInfo.get('directors'):
                    director=(detailInfo.get('directors')[0].get('peopleNm'))
                    
            
            if i.get('audiAcc'):
                audi=i.get('audiAcc')
        
            movie = Movie.objects.create(title=title, director=director, age=grade, audience=audi)
            if movieGenre:
                for genre in movieGenre:
                    tmp = Genre.objects.filter(name=genre)
                    if tmp: #장르가 있을 때
                        movie.genres.add(tmp[0])
                    else: #장르 없을 때, 그 후 저장
                        Genre.objects.create(name=genre)
                        movie.genres.add(Genre.objects.filter(name=genre)[0])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
            url = 'https://openapi.naver.com/v1/search/movie.json?query={}&yearto={}&yearfrom={}'.format(title,prdtYear,int(prdtYear)-1)
            des=""
            response = requests.get(url, headers=headers).json()
            print(response)
            if not response.get('items'):
                continue

            code=""
            for i in range(len(response.get('items')[0].get('link'))-1,-1,-1):
                
                if response.get('items')[0].get('link')[i]=="=":
                    break
                else:
                    code+=response.get('items')[0].get('link')[i]
            code=code[::-1]
            userRating=response.get('items')[0].get('userRating')
            req = requests.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code={}'.format(code))
            source = req.text
            soup=BeautifulSoup(source,'html.parser')
            # print(soup.select('#content > div.article > div.mv_info_area > div.mv_info > h3 > a')[0].text, code, url)
            des=soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')[0].text
            
            imageReq = requests.get('https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={}'.format(code))
            source = imageReq.text
            soup=BeautifulSoup(source,'html.parser')
            if soup.select('#targetImage')[0]['src']:
                movie.poster_url=soup.select('#targetImage')[0]['src']
            movie.description=des
            movie.movie_score=userRating
            # print(title,director,grade,soup.select('#targetImage')[0]['src'],des)
            # allGenres=Genre.objects.values_list('name', flat=True).distinct()
            movie.save()
        
        # 영화의 제목,연도 뽑아서 저장
        # 네이버 api에 요청
        # 나온 값 중 코드 뽑아서 다시 요청 code=****** 6글자
        # 제목 뽑은걸로 디스크립션 크롤링, 코드 뽑은걸로 포스터 크롤링
        # ?
    return redirect('movies:index')


def update(request, movie_id):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)

    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:master_index')
    else:
        form = MovieForm(instance=movie)
    context = {'form': form,}
    # embed()
    return render(request, 'movies/forms.html', context)


def delete(request, movie_id):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)

    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('movies:master_index')


def create(request):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.id)
    else:
        form = MovieForm()
    context = {
        'form': form
    }
    return render(request, 'movies/forms.html', context)


def recommend(request):
    movies = Movie.objects.all().filter(age__lte=request.user.age).order_by('-audience')[:12]
    context = {
        'movies': movies,
    }
    return render(request, 'movies/recommend.html', context)


def search(request):
    word = request.POST.get('word')
    movies = Movie.objects.all().filter(Q(title__contains=word)|Q(director__contains=word)|Q(description__contains=word)).filter(age__lte=request.user.age).order_by('-audience')
    context = {
        'movies': movies,
        'word': word,
    }
    return render(request, 'movies/searched.html', context)


def more_recommend(request, user_id):
    if request.user.is_authenticated:
        movies=Movie.objects.filter(age__lte=request.user.age)
        if request.user.is_authenticated:
            like_movies = request.user.like_movies.all()
        else:
            like_movies = []
        genres = Genre.objects.all()
        genrelist = [0 for _ in range(len(genres)+1)]
        for movie in like_movies:
            moviegenres = movie.genres.all()
            for genre in moviegenres:
                genrelist[genre.id] += 3
        reviews = request.user.reviews.all()
        for review in reviews:
            moviegenres = review.movie.genres.all()
            genre_score = review.score
            for genre in moviegenres:
                genrelist[genre.id] += genre_score
        idx = 1
        maxcnt = 0
        for i in range(len(genres)):
            if genrelist[i] > maxcnt:
                maxcnt = genrelist[i]
                idx = i

        like_genre = genres.get(id=idx)
        like_genre_movies = like_genre.movies.filter(age__lte=request.user.age).order_by('-audience')[:12]
        idx = 0
        maxcnt = 0
        context={
            'like_genre': like_genre,
            'like_genre_movies': like_genre_movies
            }
    else:
        context = {}
        
    return render(request, 'movies/more_recommend.html', context)