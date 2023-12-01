
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

import threading
import json
import ipfshttpclient
import os
import shutil
from web3 import Web3, HTTPProvider

app = Flask(__name__)
CORS(app)

# Ganache implementation
contract_address     = "0x0e3D8e15019fBB71F45b619fA38c3e90D8C96045"

trainee_private_key   = "7ba69ecf88e8a56356a29f166bf87a2aece8fac2aa1ffbee459a1258dda1ec72"
trainee       = "0x080C0B5E15FA20f520e27C6C9ebDd59cc7d20f02"
w3 = Web3(HTTPProvider("http://127.0.0.1:7545"))

training_abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "requests", "outputs": [ { "name": "demotype", "type": "string" }, { "name": "duration", "type": "uint256" }, { "name": "number", "type": "uint256" }, { "name": "rate", "type": "uint256" }, { "name": "init", "type": "bool" }, { "name": "demofile", "type": "string" }, { "name": "reward_gained", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "trainer", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "traineeAddr", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [ { "name": "_Ntua", "type": "address" }, { "name": "_traineeAddr", "type": "address" } ], "payable": true, "stateMutability": "payable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "demotype", "type": "string" }, { "indexed": false, "name": "duration", "type": "uint256" }, { "indexed": false, "name": "requestno", "type": "uint256" } ], "name": "RequestSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "rate", "type": "uint256" } ], "name": "RateSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "demofile", "type": "string" } ], "name": "DemoSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "reward_gained", "type": "uint256" } ], "name": "TrainingCompleted", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "trainer", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "amount", "type": "uint256" } ], "name": "PaymentCompleted", "type": "event" }, { "constant": true, "inputs": [ { "name": "number", "type": "uint256" } ], "name": "queryRequest", "outputs": [ { "name": "duration", "type": "uint256" }, { "name": "rate", "type": "uint256" }, { "name": "demofile", "type": "string" }, { "name": "reward_gained", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "demotype", "type": "string" }, { "name": "duration", "type": "uint256" } ], "name": "requestDemo", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "rate", "type": "uint256" } ], "name": "sendRate", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "demofile", "type": "string" } ], "name": "sendDemo", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "reward_gained", "type": "uint256" } ], "name": "trainingCompleted", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "reward_gained", "type": "uint256" } ], "name": "safePay", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_sender", "type": "address" }, { "name": "_value", "type": "uint256" }, { "name": "_tokenContract", "type": "address" }, { "name": "_extraData", "type": "bytes" } ], "name": "receiveApproval", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')

training_contract = w3.eth.contract(address=contract_address, abi=training_abi)



# IPFS client
ipfs_client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
#get the current working dir
src_dir = os.getcwd()


class mytrainee():
    def __init__(self):
        self.mlagents_url = "http://127.0.0.1:5100/"
        self.requestno = 0
        self.reward_gained = 0
        self.demohash = ""

        print("Trainee started ....")
        print("Connected: ", w3.isConnected())
        print("Contract Funsctions: ", training_contract.all_functions())


    # Server needs to:
    # 1. given the IPFS demo hash code, download, rename and 
    # store the IPFS demofile into 'Demos'folder
    # 2. initiate ml-agents's training by sending a relative request
    def download_demo(self):
        print("in download_demo")
        # Trainee downloads the demofile from IPFS
        print("Trainee downloads the demofile from IPFS ...")
        ipfs_client.get(self.demohash)
        print("Trainee SUCCESSFULLY downloaded the demofile from IPFS")

        # Copy the downloaded file to ./Demos folder
        # Rename the download file as 'demofileYYMMDDHHMMSS.demo'
        dest_dir = src_dir.replace("\\", "/") + "/Demos"

        src_file = os.path.join(src_dir, self.demohash)
        shutil.copy(src_file,dest_dir) 

        
        # Rename the download file as 'demofileYYMMDDHHMMSS.demo'
        dst_file = os.path.join(dest_dir, self.demohash)

        finalfile = self.demohash+'.demo'
        print('New filename of the demofile:', finalfile)
        new_dst_file_name = os.path.join(dest_dir, finalfile)
        os.replace(dst_file, new_dst_file_name) #rename  
        
        
        
        # Construct full path demo filename          
        demofile = dest_dir + '/' + finalfile
        print("Full pathname of the demofile")
                
        # Ask from mlagents to start the training!!!
        print("Trainee is asking mlagents to start training with demofile: ", demofile)
        message = {
            'demofile' : demofile,
        }
        r = requests.post(self.mlagents_url + "training", data=message)
        response = r.json().get("response")
        print("mlagents responded ======= ", response)
        return

    def training_completed(self):
        print("in training_completed")
        print("requestno: ", self.requestno)
        print("reward_gained: ", self.reward_gained)

        tx_hash = training_contract.functions.trainingCompleted(self.requestno, self.reward_gained).transact({'from': trainee})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt is None:
            print("@@@@@@@@@@@@@@@ request_demo trasaction call failed")
            return 

        processed_receipt = training_contract.events.TrainingCompleted().processReceipt(tx_receipt)
        print(processed_receipt)

        return


# Training Completed - Message received from ml-agents
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
  

# Training is on-going - Message received from ml-agents  
@app.route('/reward', methods = ['POST'])
def reward():
    reward = float(request.form['reward'])
    mytrainee.reward_gained = int(round(float(reward),2) * 100)

    print("----------> Reward received: ", mytrainee.reward_gained)
    response = {'response': 'OK'}
    return jsonify(response), 200

# Initiate trainig  - Message received from Trainee - UI
# Server needs to:
# 1. given the IPFS demo hash code, server downloads, renames and stores the IPFS demofile into 'Demos'folder
# 2. initiates ml-agents's training by sending a relative request
@app.route('/start_training', methods = ['POST'])
#@cross_origin(origin='localhost')
def start_training():
    print("in start_training")

    print(request)
    #demoHash = request.form.get('hash')
    data = request.get_json(force=True)
    demohash = data['demohash']
    requestno = data['requestno']
    print("demohash: ", demohash)
    print("requestno: ", requestno)

    #download_demo(demohash, self.requestno)
    mytrainee.requestno = requestno
    mytrainee.demohash = demohash
    t = threading.Thread(target=mytrainee.download_demo,args=())
    t.start()
    
    response = {'response': 'OK'}
    return jsonify(response), 200

    
if __name__ == "__main__":

    mytrainee = mytrainee()
    app.run(host='127.0.0.1', port=5200)

    