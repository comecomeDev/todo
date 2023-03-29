from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()
#몽고디비 정보입력해야함
client = MongoClient('mongodb+srv://{몽고디비 정보 입력}@cluster0.zrgxt3h.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
#SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
#import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
#import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth/signup',methods=["GET"])
def getSignup():
   return render_template('signup.html')


@app.route('/auth/signup',methods=["POST"])
def postSignup():
    #check_receive = request.args.get['id_give']
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    
    #검증(아이디 패스워드 중복 체크 및 형식 확인-서버)

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {'id':id_receive,'pw':pw_hash}
    db.user.insert_one(doc)

    #msg = request.args.get("msg")
    return jsonify({'msg': '저장완료'})    
    

@app.route('/auth/dupeCheck',methods=['GET'])
def dupeCheck():

    id_receive = request.args.get('id_give')
    user = db.user.find_one({'id' : id_receive })

    if(user is not None):
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail'})


@app.route('/auth/login',methods=['GET'])
def login():
    msg = request.args.get("msg")
    return render_template('login.html',msg=msg)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)