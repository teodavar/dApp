import threading
import time
import datetime
from web3 import Web3, HTTPProvider
import json
import asyncio
import requests
import ipfshttpclient
import os
import shutil

# IPFS client
ipfs_client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
src_dir = os.getcwd() #get the current working dir


# Ganache implementation
contract_address     = "0x0e3D8e15019fBB71F45b619fA38c3e90D8C96045"
token_address       = "0x79091CB21cd0b7a19f909806C3683BCf599Cf6eE"
trainee_private_key   = "7ba69ecf88e8a56356a29f166bf87a2aece8fac2aa1ffbee459a1258dda1ec72"
trainee       = "0x080C0B5E15FA20f520e27C6C9ebDd59cc7d20f02"
w3 = Web3(HTTPProvider("http://127.0.0.1:7545"))

training_abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "requests", "outputs": [ { "name": "demotype", "type": "string" }, { "name": "duration", "type": "uint256" }, { "name": "number", "type": "uint256" }, { "name": "rate", "type": "uint256" }, { "name": "init", "type": "bool" }, { "name": "demofile", "type": "string" }, { "name": "reward_gained", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "trainer", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "traineeAddr", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [ { "name": "_Ntua", "type": "address" }, { "name": "_traineeAddr", "type": "address" } ], "payable": true, "stateMutability": "payable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "demotype", "type": "string" }, { "indexed": false, "name": "duration", "type": "uint256" }, { "indexed": false, "name": "requestno", "type": "uint256" } ], "name": "RequestSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "rate", "type": "uint256" } ], "name": "RateSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "demofile", "type": "string" } ], "name": "DemoSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "reward_gained", "type": "uint256" } ], "name": "TrainingCompleted", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "trainer", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "amount", "type": "uint256" } ], "name": "PaymentCompleted", "type": "event" }, { "constant": true, "inputs": [ { "name": "number", "type": "uint256" } ], "name": "queryRequest", "outputs": [ { "name": "duration", "type": "uint256" }, { "name": "rate", "type": "uint256" }, { "name": "demofile", "type": "string" }, { "name": "reward_gained", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "demotype", "type": "string" }, { "name": "duration", "type": "uint256" } ], "name": "requestDemo", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "rate", "type": "uint256" } ], "name": "sendRate", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "demofile", "type": "string" } ], "name": "sendDemo", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "reward_gained", "type": "uint256" } ], "name": "trainingCompleted", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "reward_gained", "type": "uint256" } ], "name": "safePay", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_sender", "type": "address" }, { "name": "_value", "type": "uint256" }, { "name": "_tokenContract", "type": "address" }, { "name": "_extraData", "type": "bytes" } ], "name": "receiveApproval", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')
token_abi = json.loads('[ { "constant": true, "inputs": [], "name": "name", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "name": "", "type": "uint8" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "balanceOf", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "address" } ], "name": "allowance", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [ { "name": "initialSupply", "type": "uint256" }, { "name": "tokenName", "type": "string" }, { "name": "tokenSymbol", "type": "string" } ], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "from", "type": "address" }, { "indexed": true, "name": "to", "type": "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "from", "type": "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name": "Burn", "type": "event" }, { "constant": false, "inputs": [ { "name": "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "transfer", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_from", "type": "address" }, { "name": "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "approve", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_value", "type": "uint256" }, { "name": "_extraData", "type": "bytes" } ], "name": "approveAndCall", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_value", "type": "uint256" } ], "name": "burn", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_from", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "burnFrom", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')

training_contract = w3.eth.contract(address=contract_address, abi=training_abi)
token_contract = w3.eth.contract(address=token_address, abi=token_abi)

class mytrainee():
    def __init__(self):
        self.mlagents_url = "http://127.0.0.1:5100/"
        self.requestno = 0
        self.demotype = ""
        self.demofile = ""
        self.demohash = ''
        self.duration = 0
        self.reward_gained = 0
        self.rate = 0

        print("Trainee started ....")

        print("Connected: ", w3.isConnected())
        print("Contract Funsctions: ", training_contract.all_functions())

    # Server needs to:
    # 1. given the IPFS demo hash code, download, rename and 
    # store the IPFS demofile into 'Demos'folder
    # 2. initiate ml-agents's training by sending a relative request
    def start_training(self, demohash, requestno):
        print("in start_training")
        self.demohash = demohash
        self.requestno = requestno
        # Trainee downloads the demofile from IPFS
        print("Trainee downloads the demofile from IPFS ...")
        ipfs_client.get(self.demohash)
        print("Trainee SUCCESSFULLY downloaded the demofile from IPFS")

        # Copy the downloaded file to ./Demos folder
        dest_dir = src_dir.replace("\\", "/") + "/Demos"
        src_file = os.path.join(src_dir, self.demohash)
        shutil.copy(src_file,dest_dir) 

        # Rename the download file as 'demofileYYMMDDHHMMSS.demo'
        dst_file = os.path.join(dest_dir, self.demohash)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        print(st)
        finalfile = 'demofile'+st+'.demo'
        print('New filename of the demofile:', finalfile)
        new_dst_file_name = os.path.join(dest_dir, finalfile)
        os.rename(dst_file, new_dst_file_name) #rename  

        # Construct full path demo filename          
        self.demofile = dest_dir + '/' + finalfile
        print("Full pathname of the demofile")
            
        # Ask from mlagents to start the training!!!
        print("Trainee is asking mlagents to start training with demofile: ", self.demofile)
        message = {
            'demofile' : self.demofile,
        }
        r = requests.post(self.mlagents_url + "training", data=message)
        response = r.json().get("response")
        print("mlagents responded ======= ", response)
                

    def start_transaction(self):

        print("Trainee balance: ", token_contract.functions.balanceOf(trainee).call())
        
        output = "Trainee {} is sending a 'RequestDemo' to contract ...."\
            .format(trainee)
        print(output)
        self.demotype = 'demotype'
        self.duration = 4
        self.request_demo(self.demotype, self.duration)
        self.wait_for_event()

    def request_demo(self, demotype, duration):

        # use hash to query the transaction into the blockchain
        tx_hash = training_contract.functions.requestDemo(demotype, duration).transact({'from': trainee})
        # receipt is received: the transaction has been added to the blockchain
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt is None:
            print("request_demo trasaction call failed")
            return 

        processed_receipt = training_contract.events.RequestSent().processReceipt(tx_receipt)
        print(processed_receipt)
        
        '''
        output = "Address {} broadcasted the opinion: {}"\
            .format(processed_receipt[0].args._soapboxer, processed_receipt[0].args._opinion)
        print(output)
        return {'status': 'added', 'processed_receipt': processed_receipt}
        '''
        return

    # reward_gained has already been rounded up to 2 decimals
    def training_completed(self):
        print("requestno: ", self.requestno)
        print("reward_gained: ", self.reward_gained)
        tx_hash = training_contract.functions.trainingCompleted(self.requestno, self.reward_gained).transact({'from': trainee})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt is None:
            print("@@@@@@@@@@@@@@@ request_demo trasaction call failed")
            return 

        processed_receipt = training_contract.events.TrainingCompleted().processReceipt(tx_receipt)
        print(processed_receipt)

        # Solution A - two fold payment : a) approve and b) trainingCompleted

        amount = self.rate * self.reward_gained * 10 ** 4
        tx_hash = token_contract.functions.approve(contract_address, amount).transact({'from': trainee})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt is None:
            print("@@@@@@@@@@@@@@@ request_demo trasaction call failed")
            return 

        tx_hash = training_contract.functions.safePay(self.requestno, self.reward_gained).transact({'from': trainee})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt is None:
            print("@@@@@@@@@@@@@@@ request_demo trasaction call failed")
            return 

        processed_receipt = training_contract.events.TrainingCompleted().processReceipt(tx_receipt)
        print(processed_receipt)
        print("Trainee paid: ", amount)

        
        # Solution B - one fold payment : approve & trainingCompleted
        # VERY UNSTABLE SOLUTION !!!!!!
        '''
        amount = self.rate * self.reward_gained * 10 ** 4
        print("AMOUNT: ", amount)
        value = str(self.reward_gained).encode('utf-8') # .str(): converts int to str, encode: converts str to bytes
        
        tx_hash = token_contract.functions.approveAndCall(contract_address, amount, value).transact({'from': trainee})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt is None:
            print("@@@@@@@@@@@@@@@ request_demo trasaction call failed")
            return 
        print("Trainee paid: ", amount)
        '''

        return

    def handle_event(self, event):
        #print(event)
        print("EVENT RECEIVED: ", event)
        
        if event['event'] == 'RateSent':
            
            #event RateSent(address trainee, uint requestno, uint rate)
            if event['args']['trainee'] == trainee:
                print("The RateSent Event was for me!!!")
                self.requestno = event['args']['requestno']
                self.rate = event['args']['rate']

        if event['event'] == 'PaymentCompleted':
            print("The PaymentCompleted Event !!!!!")


        if event['event'] == 'Transfer':     
            print("The Transfer Event !!!!!")

        if event['event'] == 'DemoSent':
            
            #event DemoSent(address trainee, uint requestno, string demofile);
            if event['args']['trainee'] == trainee:
                print("The DemoSent Event was for me with demofile: ", event['args']['demofile'])
                self.demohash = event['args']['demofile'] # contains the hash code provided by IPFS
                #self.demohash = 'QmYYQUeYgi95LyuaRJEhreCEQAGwecugUEGg4Bk4xx93jD'
                self.demohash = 'humming03'
                print("DEMOhash: ", self.demohash)
                
                # Trainee downloads the demofile from IPFS
                '''
                print("Trainee downloads the demofile from IPFS ...")
                ipfs_client.get(self.demohash)
                print("Trainee SUCCESSFULLY downloaded the demofile from IPFS")
                '''
                # Copy the downloaded file to ./Demos folder
                dest_dir = src_dir.replace("\\", "/") + "/Demos"
                src_file = os.path.join(src_dir, self.demohash)
                shutil.copy(src_file,dest_dir) 

                # Rename the download file as 'demofileYYMMDDHHMMSS.demo'
                dst_file = os.path.join(dest_dir, self.demohash)
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
                print(st)
                finalfile = 'demofile'+st+'.demo'
                print('New filename of the demofile:', finalfile)
                new_dst_file_name = os.path.join(dest_dir, finalfile)
                os.rename(dst_file, new_dst_file_name) #rename  

                # Construct full path demo filename          
                self.demofile = dest_dir + '/' + finalfile
                print("Full pathname of the demofile")
            
                
                # Ask from mlagents to start the training!!!
                print("Trainee is asking mlagents to start training with demofile: ", self.demofile)
                message = {
                    'demofile' : self.demofile,
                }

                r = requests.post(self.mlagents_url + "training", data=message)
                response = r.json().get("response")
                print("mlagents responded ======= ", response)
                
                return    

    # 1st & 2nd try
    async def log_loop(self, event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    # 3rd try
    def log_loop(self, event_filter, poll_interval):
        print("XXXXXXXXXXXXX")
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(poll_interval)

    def wait_for_event(self):
        '''
        RateSent_filter = training_contract.events.RateSent.createFilter(fromBlock='latest')
        DemoSent_filter = training_contract.events.DemoSent.createFilter(fromBlock='latest')
        PaymentCompleted_filter = training_contract.events.PaymentCompleted.createFilter(fromBlock='latest')
        '''

        # 1st try
        '''
        loop = asyncio.get_event_loop()
        '''

        # 2nd try
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                asyncio.gather(
                    self.log_loop(RateSent_filter, 2),
                    self.log_loop(DemoSent_filter, 2)
                ))
        finally:
            loop.close()
        '''

        # 3rd try
        Transfer_filter = token_contract.events.Transfer.createFilter(fromBlock='latest')
        RateSent_filter = training_contract.events.RateSent.createFilter(fromBlock='latest')
        DemoSent_filter = training_contract.events.DemoSent.createFilter(fromBlock='latest')
        PaymentCompleted_filter = training_contract.events.PaymentCompleted.createFilter(fromBlock='latest')
    
    
        worker1 = threading.Thread(target=self.log_loop, args=(RateSent_filter, 5), daemon=True)
        worker1.start()
        worker2 = threading.Thread(target=self.log_loop, args=(DemoSent_filter, 5), daemon=True)
        worker2.start()
        worker3 = threading.Thread(target=self.log_loop, args=(PaymentCompleted_filter, 5), daemon=True)
        worker3.start()
        worker4 = threading.Thread(target=self.log_loop, args=(Transfer_filter, 5), daemon=True)
        worker4.start()


