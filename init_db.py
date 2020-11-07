import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# DB에 저장할 구두들의 출처 url을 가져옵니다.
# 네이버 예시 #old_content > table > tbody > tr:nth-child(2) > td.title > a
#오픈 API 주소: http://openapi.seoul.go.kr:8088/44426542586861723730434761786a/json/ListGeoInfoOfShoeRepairShopService/1/1000
# 구주소
# #json > ul > li > div > ul > li:nth-child(3) > div > ul > li:nth-child(1) > div > ul > li:nth-child(5) > div > span.type-string
# 지번 주소
# #json > ul > li > div > ul > li:nth-child(3) > div > ul > li:nth-child(1) > div > ul > li:nth-child(6) > div > span.type-string


def get_shoe_cleaner():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://openapi.seoul.go.kr:8088/44426542586861723730434761786a/json/ListGeoInfoOfShoeRepairShopService/1/1000', headers=headers)

    shoes = data.json()['ListGeoInfoOfShoeRepairShopService']['row']

    for shoe in shoes:
        # print(shoe)
        doc = {
            'X_COORD': shoe['X_COORD'],
            'Y_COORD': shoe['Y_COORD'],
            'gu_address': shoe['WITH_PNU_NM'],
            'detail_address': shoe['WITH_ADDR2']
        }

        db.shoes_cleaner.insert_one(doc)


# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.shoes_cleaner.drop()  # mystar 콜렉션을 모두 지워줍니다.
    get_shoe_cleaner()


### 실행하기
insert_all()