from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

def index(request):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)

    return render(request, 'movie_master/index.html')


def getdata(request):
    if not request.user.is_superuser:
        return HttpResponse('401 Unauthorized Access', status=401)

    return render(request, 'movie_master/getdata.html')