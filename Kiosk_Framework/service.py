from flask import Flask, request, request, redirect, url_for, render_template
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


@app.route('/menu', methods=['POST'])
def menu():
    order_type = request.form.get("type")
    return render_template("menu.html")

@app.route('/option', methods = ['POST'])
def option():
    name = request.form.get("name")
    type = request.form.get("type")
    return render_template("option.html")

@app.route('/purchase', methods = ['POST'])
def purchase():
    data = request.form.get("data")
    return render_template("purchase.html")


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