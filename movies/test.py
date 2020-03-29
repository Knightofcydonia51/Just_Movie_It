# import codecs
# encoded = codecs.open('movies.json', 'r', 'utf-8').read().encode(
#             'ascii', 'backslashreplace')
# open('movies.json', 'w').write(encoded)3

from datetime import timedelta, datetime
from decouple import config
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


day1='20190120'
day2='20191101'
print(int(day1[:4]),int(day1[4:6]),int(day1[6:]))
day1 = datetime(int(day1[:4]),int(day1[4:6]),int(day1[6:]))
day2 = datetime(int(day2[:4]),int(day2[4:6]),int(day2[6:]))
days=(day2-day1).days
print(days//7)

for i in range(days//7):
    day2=day2-timedelta(weeks=i)
    print(day2)
    targetDt=day2.strftime('%Y%m%d')
    print(targetDt)
key=config('API_KEY')



# for i in range(30):
# t_time=t_time.strftime('%Y%m%d')
# time_cnt=now-datetime.timedelta(weeks=week)
# targetDt=time_cnt.strftime('%Y%m%d')


# boxoffice50 = requests.get('http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=430156241533f1d058c603178cc3ca0e&targetDt=20120101')
# box = boxoffice50.json().get('boxOfficeResult').get('weeklyBoxOfficeList')
# print(box[0])
# print(box[1])


# movieInfo={    
# "audits":[
#     {
#         "auditNo": "2012-F610",
#         "watchGradeNm": "15세이상관람가"
#         }
#     ],
# "genres": [
#         {
#             "genreNm": "사극"
#         },
#         {
#             "genreNm": "드라마"
#         },
#         {
#             "genreNm": "액션"
#         }
#     ]}


# print(movieInfo.get('audits')[0].get('watchGradeNm'))
# for i in range(len(movieInfo.get('genres'))):
#     print(movieInfo.get('genres')[i].get('genreNm'),len(movieInfo.get('genres')))

# NAVER_CLIENT_ID=config('NAVER_CLIENT_ID')
# NAVER_CLIENT_SECRET=config('NAVER_CLIENT_SECRET')
# headers = {
#     'X-Naver-Client-Id' : NAVER_CLIENT_ID,
#     'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
#     }  

# print(naverKey,Secret)

# req = requests.get('https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=119491')
# html=req.text
# soup=BeautifulSoup(html,'html.parser')
# soupsoup=soup.select('#targetImage')
# print(soupsoup[0])
# print(soupsoup[0]['src'])
# code=20124079
# now=datetime.datetime.now() #.strftime('%Y%m%d')
# now=now-datetime.timedelta(weeks=1)
# now=now.strftime('%Y%m%d')
# print(now)
# movieDetail='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={}&targetDt={}'.format(key,now)
# response=requests.get(url=movieDetail)
# info=response.json()
# print(info.get('boxOfficeResult').get('weeklyBoxOfficeList')[0])
# for i in info.get('boxOfficeResult').get('weeklyBoxOfficeList'):
#     for k,v in i.items():
#         print(k)


# title,prdtYear="두번할까요","2018"
# url = 'https://openapi.naver.com/v1/search/movie.json?query={}&yearto={}&yearfrom={}'.format(title,prdtYear,prdtYear)
# response = requests.get(url, headers=headers).json()
# print(response)
# print('hi')
# if response.get('items'):
#     code=""
#     print(response.get('items')[0].get('link'))
#     for i in range(len(response.get('items')[0].get('link'))-1,-1,-1):
#         print(response.get('items')[0].get('link')[i])
#         if response.get('items')[0].get('link')[i]=="=":
#             break
#         else:
#             code+=response.get('items')[0].get('link')[i]
#     code=code[::-1]
    
#     req = requests.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code={}'.format(code))
#     source = req.text
#     soup=BeautifulSoup(source,'html.parser')
#     # print(soup.select('#content > div.article > div.mv_info_area > div.mv_info > h3 > a')[0].text, code, url)
#     # print(soup)
#     print(code)
#     # print(soup)
#     des=soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')[0].text
#     print(des)

#     imageReq = requests.get('https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={}'.format(code))
#     source = imageReq.text
#     soup=BeautifulSoup(source,'html.parser')
#     print(soup.select('#targetImage')[0]['src'])
    
    

