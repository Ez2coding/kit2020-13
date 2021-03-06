
from flask import Flask, request, render_template, redirect, url_for, abort
from tkinter import messagebox as msg
from tkinter import Tk

import game
import json

import dbdb

app = Flask(__name__)



@app.route('/')
def index():
    return render_template("main.html") 

@app.route('/hello')
def hello():
    return 'Hello, world!'


@app.route('/hello/<name>')
def hellovar(name):
    character = game.set_charact(name)
    return render_template("gamestart.html", data = character )

@app.route('/gamestart')
def gamestart():
    with open("static/save.txt", "r", encoding='utf-8') as f:
        data = f.read()
        character = json.loads(data)
        print(character["AA"])
    return "{}이 {}를 사용해서 이겼다." .format(character["닉네임"], [character["AA"]]) 



@app.route('/input/<int:num>')    
def input_num(num):
    if num == 1:
        with open("static/save.txt", "r", encoding='utf-8') as f:
            data = f.read()
            character = json.loads(data)
            print(character["스킬"])
        return "{}이 {}를 사용해서 이겼다." .format(character["닉네임"], [character["AA"]][0]) 
    elif num == 2:        
        return "도망갔다"
    elif num ==3:
        name = '퉁퉁이'
    else:
        return "없어요"
    return "hello {}".format(name)

# # 로그인
# @app.route('/login')
# def login2():
#     return render_template('login.html') 

@app.route('/method', methods=['GET', 'POST'])    
def method2():
    if request.method == 'GET':
        return "GET으로 전달된 데이터"
     
    else:
        id = request.form['id']
        pw = request.form['pw']
        print (id,type(id))
        print (pw,type([pw]))
        # id 와 pw가 db 값이랑 비교해서 맞으면 맞다 틀리면 틀리다
        ret = dbdb.select_user(id, pw)
        if ret != None:
            return "안녕하세요~ {}님".format(id)
        else:
            return "아이디 또는 패스워드를 확인하세요."
        # if (id == 'aaa' and pw == '1234'):
        #     return "안녕하세요~ {} 님".format(id)
            # print(id, pw)
            # root= Tk()
            # root.withdraw()
            # return msg.showinfo('로그인 성공!' ,'아이디: {} 패스워드: {}'.format(id, pw))
        # else:
            # return "잘못 입력하셨습니다."
            # root= Tk()
            # root.withdraw()
            # return msg.showinfo("로그인 실패", "잘못 입력하셨습니다.")

# 로그인 
@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'GET': 
        return render_template('login.html') 
    else: 
        id = request.form['id'] 
        pw = request.form['pw'] 
        print(id, type(id))
        print(pw, type(pw))
        
        # id와 pw가 임의로 정한 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다 
        ret = dbdb.select_user(id, pw)
        print(ret[2])
        if ret != None:
            return "안녕하세요~ {}님".format(ret[2])
        else:
            return "아이디 또는 패스워드를 확인하세요."
        



#회원가입
@app.route('/join', methods=['GET', 'POST'])    
def join():
    if request.method == 'GET':
        return render_template('join.html')
     
    else:
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        print (id,type(id))
        print (pw,type(pw))

        ret = dbdb.check_id(id)
        if ret != None:
            return '''
                    <script>
                    alert('다른 아이디를 사용하세요');
                    location.href='/join';
                    </script>
                   '''
        # id 와 pw가 db 값이랑 비교해서 맞으면 맞다 틀리면 틀리다
        dbdb.insert_user(id, pw, name)
        return redirect(url_for('login'))
        
@app.route('/form')
def form():
    return render_template('test1.html')


@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return 'GET으로 전송이다'
    else:
        num = request.form['num']
        name = request.form['name']
        print(num, name)
        dbdb.insert_data(num, name)
        return 'POST 이다 학번은: {} 이름은: {} '.format(num, name)

@app.route('/getinfo')        
def getinfo():
    ret = dbdb.select_all()
    print(ret[3])
    return render_template('getinfo.html', data = ret )
    # return '번호 : {}, 이름: {}'.format(ret[0], ret[1])


@app.route('/naver')    
def naver():
    return render_template("naver.html")

@app.route('/daum')
def daum():
    return redirect("https://www.daum.net/")

@app.route('/move/daum')
def url_test():
    return redirect(url_for('daum'))


@app.route('/move/naver')
def url_test2():
    return redirect(url_for('naver'))


@app.route('/img')
def img():
    return render_template("image.html")

@app.route('/urltest')
def url_test3():
    return redirect(url_for('naver'))

@app.route('/move/<site>')    
def move_site(site):
    if site == 'naver':
        return redirect(url_for('naver'))
    elif site == 'daum':
        return redirect(url_for('daum'))
    else: 
        return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return "페이지가 없습니다. URL을 확인하세요." , 404


if __name__ == '__main__':
    # with app.test_request_context():
    #     print(url_for('daum'))
    #     print(url_for('naver'))
    app.run(debug=True)
