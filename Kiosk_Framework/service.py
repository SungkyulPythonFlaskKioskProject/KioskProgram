from flask import Flask, request, redirect, url_for, render_template,jsonify,url_for,session
import json
from json import JSONEncoder
import numpy
import os, logging

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static', ## 정적 폴더 위치, default로 index.html을 불러옴
    template_folder='./templates' ##템플릿 파일 기본 폴더
)

app.secret_key = 'aaaaaa'

## 초기 설정
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

################################################################################
## 여기에 필요한 기능 코드 작성

## 주문
@app.route('/kiosk_page/order', methods=['POST'])
def order():
    logDisable(False) ## 로그 저장

    order_menu = request.form["order"]
    fileSave(order_menu)
    output = {"output": "none"}
    output = json.dumps(output, cls=NumpyArrayEncoder)
    return outputJSON(json.loads(output), "ok")




@app.route('/menu', methods=['POST','GET'])
def menu():
    return render_template("menu.html")

#Post일때는 name,type 저장 후 menu로 redirect, Get일때는 order type json 형식으로 반환
@app.route('/getIndex', methods=['POST','GET'])
def getIndex():
    if request.method == 'POST':
        order_type = request.form.get("type")
        session['orderType'] = order_type
        return redirect(url_for('menu'))
    


#Post일때는 name,type 저장 후 option로 redirect, Get일때는 name 과 type json 형식으로 반환
@app.route('/getMenu', methods=['POST','GET'])
def getMenu():
    if request.method == 'POST':
        name = request.form.get("name")
        type = request.form.get("type")
        session['name'] = name
        session['type'] = type
        return redirect(url_for('option'))
    

#option으로 이동
@app.route('/option', methods = ['POST','GET'])
def option():
    return render_template("option.html")

#Post일때는 data 저장 후 purchase로 redirect, Get일때는 data json 형식으로 반환
@app.route('/getOption', methods=['POST','GET'])
def getOption():
    if request.method == 'POST':
        data = request.form.get("data")
        session['option'] = data
        return redirect(url_for('purchase'))
    


#purchase로 이동
@app.route('/purchase', methods = ['POST','GET'])
def purchase():
    return render_template("purchase.html")


@app.route('/getData', methods = ['POST','GET'])
def getData():
    order_type = session.get('orderType', '')
    name = session.get('name', '')
    type = session.get('type', '')
    option = session.get('option', '')
    data = jsonify({"name": name,"orderType": order_type,"type": type,"option": option})
    return data



## 주문 정보 가지고 오기
@app.route('/kitch_page/getOrder', methods=['POST'])
def getOrder(): 
    logDisable(True) ## 로그 저장 X

    currentOrder = os.listdir('./data')
    output = {"output": currentOrder}
    output = json.dumps(output, cls=NumpyArrayEncoder)
    return outputJSON(json.loads(output), "ok")

################################################################################
## 테스트 코드: 참고용
@app.route('/kiosk_page/test', methods=['POST'])
def test():
    output = request.form["name"]
    output = {"output": output}
    output = json.dumps(output, cls=NumpyArrayEncoder)
    return outputJSON(json.loads(output), "ok")

def fileSave(content):
    path = './data'
    f = open(f'{path}/{content}.txt', 'w')
    f.write('test-test')
    f.close()

def logDisable(n):
    log = logging.getLogger('werkzeug')
    log.disabled = n 

def outputJSON(msg, status="error"):
    return {"data": msg, "status": status}

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

if __name__ == '__main__':
    app.run(debug=True)