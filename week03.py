#150위까지 출력
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.genieList    # 'dbsparta'라는 이름의 db를 사용합니다. 'dbsparta' db가 없다면 새로 만듭니다.


# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

a = 0;
for i in range(1,4):
    url = 'https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200713&hh=23&rtm=N&pg=' + str(i)
    print (url)
    data = requests.get(url, headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    # soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
    # 이제 코딩을 통해 필요한 부분을 추출하면 된다.
    soup = BeautifulSoup(data.text, 'html.parser')

    #############################
    # (입맛에 맞게 코딩)
    #############################

    # select를 이용해서, tr들을 불러오기
    songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
    #body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td.number

    #body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td.info > a.title.ellipsis
    #body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td.info > a.artist.ellipsis
    # movies (tr들) 의 반복문을 돌리기
    for song in songs:
        # movie 안에 a 가 있으면,
        rank = song.select_one('td.number').text[0:3].strip()
        title = song.select_one('td.info > a.title.ellipsis').text.strip()
        artist = song.select_one('td.info > a.artist.ellipsis').text.strip()
       # a_tag.text.strip()
        print(rank, title , artist)
        doc = {
            'rank': rank,
            'title': title,
            'artist': artist  # DB에는 숫자처럼 생긴 문자열 형태로 저장됩니다.
        }
        db.genieList.insert_one(doc)