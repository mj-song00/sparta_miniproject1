from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

import jwt

client = MongoClient('mongodb+srv://test:sparta@Cluster0.faljs.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAfile=ca)
db = client.blogsparta

SECRET_KEY = 'HANGHAE'
@app.route('/road')
def home1():
    return render_template('index.html')

@app.route('/blog/saveBlog', methods=['GET'])
def save_blog():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(payload, SECRET_KEY, algorithm='HS256')
        url_receive = request.form['url_give']
        summary_receive = request.form['summary_give']
        like_receive = []
        comment_receive = []

    return jsonify({'msg' : '저장 완료 !!'})

@app.route('/bikeroad', methods=['POST'])
def web_bikeroad_post():
    name_receive = request.form['name_give']
    road_receive = request.form['road_give']
    difficult_receive = request.form['difficult_give']
    doc = {

        'name':name_receive,
        'road':road_receive,
        'difficult':difficult_receive
    }

    db.bikeroad.insert_one(doc)

    return jsonify({'msg':'기록 완료!'})


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/applefarm')
def home3():
    return render_template('applefarm.html')

@app.route('/order', methods=['POST'])
def order_post():
    goods_receive = request.form['goods_give']
    num_receive = request.form['num_give']
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    doc = {
        'goods':goods_receive,
        'num':num_receive,
        'name':name_receive,
        'address':address_receive,
        'phone':phone_receive
    }

    db.applefarm.insert_one(doc)

    return jsonify({'msg': '주문 완료!'})

@app.route('/order', methods=['GET'])
def order_get():
    orders_list = list(db.applefarm.find({}, {'_id': False}))
    return jsonify({'orders': orders_list})

# 박태형
client_btae = MongoClient('mongodb+srv://test:sparta@Cluster0.faljs.mongodb.net/Cluster0?retryWrites=true&w=majority')
db_tae = client_btae.food

# 메인페이지 & 저장페이지
@app.route('/food')
def food_home():
    return render_template('food.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)