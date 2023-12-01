import time
from web3 import Web3, HTTPProvider
import json
import asyncio
import ipfshttpclient

# IPFS client
ipfs_client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')

# Ganache implementation
contract_address        = "0x0e3D8e15019fBB71F45b619fA38c3e90D8C96045"
token_address       = "0x79091CB21cd0b7a19f909806C3683BCf599Cf6eE"
trainer_private_key     = "76164252b7a76d08d18ed7a68142632bc385352af01ae041f9fb7cb5e2c56037"
trainer                 = "0x5386aCc4c29E5Dd07842bBE5324590BE95FEf66C"
w3 = Web3(HTTPProvider("http://127.0.0.1:7545"))


training_abi = json.loads('[ { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "requests", "outputs": [ { "name": "demotype", "type": "string" }, { "name": "duration", "type": "uint256" }, { "name": "number", "type": "uint256" }, { "name": "rate", "type": "uint256" }, { "name": "init", "type": "bool" }, { "name": "demofile", "type": "string" }, { "name": "reward_gained", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "trainer", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "traineeAddr", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [ { "name": "_Ntua", "type": "address" }, { "name": "_traineeAddr", "type": "address" } ], "payable": true, "stateMutability": "payable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "demotype", "type": "string" }, { "indexed": false, "name": "duration", "type": "uint256" }, { "indexed": false, "name": "requestno", "type": "uint256" } ], "name": "RequestSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "rate", "type": "uint256" } ], "name": "RateSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "demofile", "type": "string" } ], "name": "DemoSent", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "reward_gained", "type": "uint256" } ], "name": "TrainingCompleted", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name": "trainee", "type": "address" }, { "indexed": false, "name": "trainer", "type": "address" }, { "indexed": false, "name": "requestno", "type": "uint256" }, { "indexed": false, "name": "amount", "type": "uint256" } ], "name": "PaymentCompleted", "type": "event" }, { "constant": true, "inputs": [ { "name": "number", "type": "uint256" } ], "name": "queryRequest", "outputs": [ { "name": "duration", "type": "uint256" }, { "name": "rate", "type": "uint256" }, { "name": "demofile", "type": "string" }, { "name": "reward_gained", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "demotype", "type": "string" }, { "name": "duration", "type": "uint256" } ], "name": "requestDemo", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "rate", "type": "uint256" } ], "name": "sendRate", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "demofile", "type": "string" } ], "name": "sendDemo", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "reward_gained", "type": "uint256" } ], "name": "trainingCompleted", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "requestno", "type": "uint256" }, { "name": "reward_gained", "type": "uint256" } ], "name": "safePay", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_sender", "type": "address" }, { "name": "_value", "type": "uint256" }, { "name": "_tokenContract", "type": "address" }, { "name": "_extraData", "type": "bytes" } ], "name": "receiveApproval", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')
token_abi = json.loads('[ { "constant": true, "inputs": [], "name": "name", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "name": "", "type": "uint8" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "balanceOf", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" }, { "name": "", "type": "address" } ], "name": "allowance", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [ { "name": "initialSupply", "type": "uint256" }, { "name": "tokenName", "type": "string" }, { "name": "tokenSymbol", "type": "string" } ], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "from", "type": "address" }, { "indexed": true, "name": "to", "type": "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "from", "type": "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name": "Burn", "type": "event" }, { "constant": false, "inputs": [ { "name": "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "transfer", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_from", "type": "address" }, { "name": "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "approve", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_value", "type": "uint256" }, { "name": "_extraData", "type": "bytes" } ], "name": "approveAndCall", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_value", "type": "uint256" } ], "name": "burn", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_from", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "burnFrom", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')
training_contract = w3.eth.contract(address=contract_address, abi=training_abi)
token_contract = w3.eth.contract(address=token_address, abi=token_abi)

expected_amount = 0
rate = 4

def send_demo(requestno, demofile):

    output = "Trainer {} is sending a 'sendDemo' to contract ...."\
        .format(trainer)
    print(output)

    # use hash to query the transaction into the blockchain
    tx_hash = training_contract.functions.sendDemo(requestno, demofile).transact({'from': trainer})
    # receipt is received: the transaction has been added to the blockchain
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    if tx_receipt is None:
        print("request_demo trasaction call failed")
        return 

    processed_receipt = training_contract.events.DemoSent().processReceipt(tx_receipt)
    print("Trainer received back : ", processed_receipt)
    
    '''
    output = "Trainer {} broadcasted the opinion: {}"\
        .format(processed_receipt[0].args._soapboxer, processed_receipt[0].args._opinion)
    print(output)
    return {'status': 'added', 'processed_receipt': processed_receipt}
    '''
    return

def send_rate(requestno, rate):

    output = "Trainer {} is sending a 'SendRate' to contract ...."\
        .format(trainer)
    print(output)

    # use hash to query the transaction into the blockchain
    tx_hash = training_contract.functions.sendRate(requestno, rate).transact({'from': trainer})
    # receipt is received: the transaction has been added to the blockchain
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    if tx_receipt is None:
        print("request_demo trasaction call failed")
        return 

    processed_receipt = training_contract.events.RateSent().processReceipt(tx_receipt)
    print("Trainer received back : ", processed_receipt)

    # Trainer prepares demo: TBD
    '''
    # Trainer uploads demo to IPFS (ipfs.infura.io)
    print("Trainer uploads demo to IPFS (ipfs.infura.io) ....")
    res = ipfs_client.add('ExpertPyramidTeo.demo')
    # demofile: contains the has code provided by IPFS
    demofile = res['Hash']
    ''' 
    demofile = 'QmYYQUeYgi95LyuaRJEhreCEQAGwecugUEGg4Bk4xx93jD'
    print("Uploaded demo has hash code: ", demofile)
    # Trainer sends the 'SendDemo' message to contract
    send_demo(requestno, demofile) 
    
    '''
    output = "Trainer {} broadcasted the opinion: {}"\
        .format(processed_receipt[0].args._soapboxer, processed_receipt[0].args._opinion)
    print(output)
    return {'status': 'added', 'processed_receipt': processed_receipt}
    '''
    return


def handle_event(event):
    #print(event)
    print("EVENT RECEIVED: ", event)

    if event['event'] == 'RequestSent':
        send_rate(event['args']['requestno'], rate)
    
    if event['event'] == 'TrainingCompleted':
        reward_gained = event['args']['reward_gained']
        expected_amount = rate * reward_gained * 10 ** 4
        print("Training Completed event received! Expected amount is: ", expected_amount)

    if event['event'] == 'Transfer':
        print("TRANSFER RECEIVED !!!!!!!")

    if event['event'] == 'PaymentCompleted':     
        if event['args']['trainer'] == trainer:
            print("The PaymentCompleted Event was for me!!!")
            print("PaymentCompleted for amount: ", event['args']['amount'])

  

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

def wait_for_event():
    
    RequestSent_filter = training_contract.events.RequestSent.createFilter(fromBlock='latest')
    TrainingCompleted_filter = training_contract.events.TrainingCompleted.createFilter(fromBlock='latest')
    
    Transfer_filter = token_contract.events.Transfer.createFilter(fromBlock='latest')
    PaymentCompleted_filter = training_contract.events.PaymentCompleted.createFilter(fromBlock='latest')
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(RequestSent_filter, 2),
                log_loop(TrainingCompleted_filter, 2),
                log_loop(Transfer_filter, 2),
                log_loop(PaymentCompleted_filter, 2)
            ))
                

    finally:
        loop.close()


if __name__ == "__main__":
    print("Connected: ", w3.isConnected())
    print("Contract Funsctions: ", training_contract.all_functions())
    
    print("Trainer balance: ", token_contract.functions.balanceOf(trainer).call())

    wait_for_event()

