
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

def learning():
    sleep(3)
    message = {'reward' : 1.325454524545654}
    r = requests.post("http://127.0.0.1:5200/reward", data=message)
    response = r.json().get("response")
    print("Trainee responded ======= ", response)
    sleep(3)
    message = {'reward' : 1.325454524545654}
    r = requests.post("http://127.0.0.1:5200/reward", data=message)
    response = r.json().get("response")
    print("Trainee responded ======= ", response)
    sleep(3)
    message = {'training' : 'completed'}
    r = requests.post("http://127.0.0.1:5200/completion", data=message)
    response = r.json().get("response")
    print("Trainee responded ======= ", response)

@app.route('/training', methods = ['POST'])
def training():

    learning()
    response = {'response': 'OK'}
    return jsonify(response), 200
  


if __name__ == "__main__":



    app.run(host='127.0.0.1', port=5100)

    


