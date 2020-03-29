from .base import *
from decouple import config 

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['last-movie-pjt.xwqm6jpu2p.ap-northeast-2.elasticbeanstalk.com']