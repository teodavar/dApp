
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import trainee
import threading

app = Flask(__name__)
CORS(app)


@app.route('/completion', methods = ['POST'])
def completion():
    training = request.form['training']
    print("----------> Training completed with status: ", training)
    # Upon training completion, trainee sends 'TrainingCompleted' to contract
    print("Trainee is sending a TrainingCompleted message to contract ....")
    print("request no: ", mytrainee.requestno)
    mytrainee.training_completed()

    response = {'response': 'OK'}
    return jsonify(response), 200
    

    

    
@app.route('/reward', methods = ['POST'])
def reward():
    reward = request.form['reward']
    mytrainee.reward_gained = int(round(float(reward),2) * 100)
    print("----------> Reward received: ", mytrainee.reward_gained)
    response = {'response': 'OK'}
    return jsonify(response), 200



if __name__ == "__main__":

    '''
    # Run without blockchain -- 1st try
    demofile = "Project/Assets/ML-Agents/Examples/Pyramids/Demos/ExpertPyramidTeo.demo"
    print("Trainee is asking mlagents to start training with demofile: ", demofile)
    mlagents_url = "http://127.0.0.1:5100/"
    message = {'demofile' : demofile}
    r = requests.post(mlagents_url + "training", data=message)
    response = r.json().get("response")
    print("Nodes port ======= ", response)
    '''

    # 3rd try
    mytrainee = trainee.mytrainee()
    mytrainee.start_transaction()
    app.run(host='127.0.0.1', port=5200)
    
    # Stucks for ever (Cntl C) -- 2nd try
    '''
    mytrainee = trainee.mytrainee()
    t = threading.Thread(target=mytrainee.start_transaction,args=())
    t.start()
    app.run(host='127.0.0.1', port=5200)
    '''
    
    # Stucks for ever (Cntl C) -- 2nd try
    '''
    t = threading.Thread(target=app.run,args=('127.0.0.1', 5200))
    t.start()
    mytrainee = trainee.mytrainee()
    mytrainee.start_transaction()
    '''
    


