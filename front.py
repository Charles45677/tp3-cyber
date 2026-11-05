from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2

app = Flask('FrontEnd')

BACK_END_IP = 'be'
BACK_END_PORT = '5555'

def build_home_page(messages):
       

        return '''<html>
        <header></header>
        <p> Bravo , tu est arrivé à lancer les conteneurs. Bonne chance pour le reste. :) </p>
        </body>
        </html>'''


def build_response(response):
        if response.status_code == 200:
                obj = json.loads(response.content.decode('utf-8'))
                resp = make_response(build_home_page(obj))
                return resp
        else:
                msg = response.content.decode('utf-8')
                resp = make_response(build_home_page({'message':msg}))
                return resp


@app.route('/')
def hello():
        return build_home_page({})


@app.route('/createuser', methods=['POST'])
def createuser():
        data = {'name': request.form['name'], 'password': request.form['password'], 'ip': request.remote_addr}
        print(data, flush=True)
        resp = requests.post('http://' + BACK_END_IP + ':' + BACK_END_PORT + '/user', json=data)
        return build_response(resp)

@app.route('/viewusers', methods=['GET'])
def viewUsers():
        data = {'ip':request.remote_addr}
        response = requests.get('http://' + BACK_END_IP + ':' + BACK_END_PORT + '/user', json=data)
        return build_response(response)



@app.route('/login', methods=['POST'])
def login():
#       ip = request.remote_addr
#       data = {'ip':ip}
#       response = requests.post('http://' + BACK_END_IP + ':' + BACK_END_PORT + '/login', auth=(request.form['username'], request.form['password']), json=data)
#       resp = build_response(response)
#
#       if response.status_code == 200:
#               obj = json.loads(response.content.decode('utf-8'))


        resp = build_home_page("the Login route is currently not available")
        return resp

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=15556)