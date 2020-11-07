from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')

def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    guName_receive = request.form['guName_give']  # 클라이언트로부터 url을 받는 부분

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(guName_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    shoes = {'guName': guName_receive}

    # 3. mongoDB에 데이터를 넣기
    # db.dbsparta.insert_one(shoes_cleaner)
    db.shoes_cleaner.insert_one(shoes)

    return jsonify({'result': 'success'})


@app.route('/shoes', methods=['GET'])
def data_get():
    guName_receive = request.args.get('guName_give')
    print(guName_receive)
    # guName_include = guName_receive + "*"
    result = list(db.shoes_cleaner.find({'gu_address':{'$regex':guName_receive}}, {'_id': 0}))
    # db.users.findOne({"username": {$regex: ".*son.*"}});

    print(result)
    return jsonify({'result': 'success', 'data': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)