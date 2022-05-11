from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)
from pymongo import MongoClient
import jwt
from bs4 import BeautifulSoup
import datetime
import hashlib
from datetime import datetime, timedelta
from bson.objectid import ObjectId


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
# 아래 URL을 본인의 몽고DBURL로 변경후 test 해주세요
mongodburl = 'mongodb+srv://test:sparta@Cluster0.faljs.mongodb.net/Cluster0?retryWrites=true&w=majority'
client = MongoClient(mongodburl)
db = client.dbsparta_plus_miniproject_real

SECRET_KEY = 'HANGHAE'


@app.route('/')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('main.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# 블로그 저장
@app.route('/blog/saveBlog', methods=['POST'])
def save_blog():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithm=['HS256'])
        user_info = db.userdb.find_one({'id': payload['id']})
        writer_name = user_info['id']  # 토큰에서 ID 정보 가져오기

        url_receive = request.form['url_give']
        desc_receive = request.form['desc_give']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')

        image = og_image['content']
        title = og_title['content']

        doc = {
            'blog_desc': desc_receive,
            'url': url_receive,
            'image': image,
            'title': title,
        }

        client.blogs.bloglist.insert_one(doc)
        return jsonify({'msg': '저장 완료 !!'})

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 올바르지 않습니다."))


# # 저장된 블로그 불러오기
# @app.route('/<url>')
# def show_clicked_post(url):
#     token_receive = request.cookies.get('mytoken')
#     print(token_receive)
#
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.userdb.find_one({'id': payload['id']})
#         user_id = user_info['id']
#
#         data = db.bloglist.find_one({'id': id, })
#         user_id = data['user_id']
#         url = data['url']
#         blog_desc = data['blog_desc']
#         image = data['image']
#         title = data['title']
#
#         return render_template("main.html",
#                                user_id=user_id,
#                                url=url,
#                                blog_desc=blog_desc,
#                                image=image,
#                                title=title)
#
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 올바르지 않습니다."))
#
#     # bloglist = list(client.blogs.bloglist.find({},{'_id':False}))
#
#     # return jsonify({'blogs':bloglist})

# 블로그 추가 저장

@app.route('/blogg')
def blogg():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({'id': payload['id']})  # 토큰을 통해 유저 정보 확인
        blog_info = list(db.blog.find())
        return render_template('index1.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))



    ##### 임시
@app.route('/bloggcomment')
def blogg_comment():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']})  # 토큰을 통해 유저 정보 확인
        user_id = user_info['username'] # 유저 id

        blog_info = list(db.blogs.find())
        return render_template('index2.html' , id=blog_info[0] )
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

    ### 임시


@app.route('/blogg/saveBlog', methods=['POST'])
def save_blogg():
    token_receive = request.cookies.get('mytoken') #토큰 받기
    print(token_receive)

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        user_info = db.users.find_one({'username': payload['id']}) # 토큰을 통해 유저 정보 확인
        print(user_info)
        user_id = user_info['username'] # 유저 id
        date_receive = request.form['date_give']
        url_receive = request.form['url_give']
        summary_receive = request.form['summary_give'] # ajax로 받은 데이터, 블로그 url, 요약, 추가 날짜
        like_receive = [] # 좋아요 추가 할 빈 리스트
        comment_receive = [] # 댓글 추가 할 빈 리스트
        doc = {
            'date': date_receive,
            'username': user_id,
            'url': url_receive,
            'summary': summary_receive,
            'likes': like_receive,
            'comments': comment_receive
        }
        db.blogs.insert_one(doc)
        return jsonify({'msg': '저장 완료 !!'})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

# 해당 블로그 삭제 '_id'값으로 비교
@app.route('/delBlog', methods=['POST'])
def del_blog():
    id_receive = request.form['id_give'] # 해당 블로그 '_id' 값
    print(id_receive)
    db.blog.delete_one({'_id': ObjectId(id_receive)}) # 블로그 db에서 삭제

    return jsonify({'msg' : '삭제되었습니다!'})

# 댓글 작성
@app.route('/savecomment', methods=['POST'])
def save_comment():
    token_receive = request.cookies.get('mytoken')  # 토큰 받기
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['id']})  # 토큰을 통해 유저 정보 확인
        user_id = user_info['username']  # 유저 id
        id_receive = request.form['id_give']  # 댓글 달 블로그 '_id'
        date_receive = request.form['date_give'] # 작성 날짜
        comment_receive = request.form['comment_give'] # 작성 글
        docs = {
            'user': user_id,
            'date': date_receive,
            'comment': comment_receive
        }  # comment에 저장될 딕셔너리
        blog = db.blogs.find_one({'_id': ObjectId(id_receive)})  # 등록할 블로그 찾기
        comment_dict = blog['comments']
        comment_dict.append(docs)
        db.blogs.update_one({'_id': ObjectId(id_receive)}, {'$set': {'comments': comment_dict}})  #블로그 comment에 추가 된 딕셔너리 추가 및 db 수정
        return jsonify({'msg': '댓글 달기 성공 !!'})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/delcomment', methods=['POST'])
def del_comment():
    listNum_receive = request.form['listNum_give']  # 댓글 리스트 번호
    id_receive = request.form['_id_give']  # 해당 블로그 '_id'
    blog_info = db.blog.find_one({"_id": ObjectId(id_receive)})
    comment_list = blog_info['comment'] #  블로그 찾고 해당 comment 리스트 가져오기
    comment_list.remove(comment_list[int(listNum_receive)])
    db.blog.update_one({'_id': ObjectId(id_receive)}, {'$set': {'comment': comment_list}})  # 댓글 삭제 및 변경된 값 수정

    return jsonify({'msg' : '삭제되었습니다!'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)