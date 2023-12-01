# 'truffle-training' project
Implements the dApp application.

# Getting Started

## dApp installation
1. Download the project and unzip it to a folder

## Ganache installation & Setting up a workspace
1. Follow the instructions https://www.trufflesuite.com/docs/ganache/quickstart

## Contract deployment via Truffle console
1. Open a windows command prompt and navigate to the root of the project
2. Install truffle by running: npm install -g truffle
3. Open truffle console by running: truffle console
4. Deploy smart contracts by running: migrate

## Tranfer Ntua tokens to Trainee agent (via Metamask)
1. Install Metamask Chrome extension according to https://metamask.io/
2. For simplicity, the first Ganache default account is assigned to trainer while the last Ganache default account is assigned to trainee.
3. Create the trainer's Metamask account and link it to the relevant Ganache account
4. Add to the trainer's Metamask account the Ntua token
5. Create the trainee's Metamask account and link it to the relevant Ganache account
6. Add to the trainee's Metamask account the Ntua token
7. Transfer 100 Ntua tokens from trainer's account to trainee's account

## Run backend trainee server: server.py
1. From the windows command prompt, navigate to the project's root
2. cd server and run : python server.py

## Run extended mlagents platform
1. Follow the intructions from the relevant github sub-repository.

## Install and Run trainee and trainer frontend
1. From the windows command prompt, navigate to the project's root, and run:
	cd client\trainee
	npm install
    npm run dev
	cd ..\trainer
	npm install
    npm run dev

# Project layout

Contains the following folders:
## 1. contracts/ folder
Contains the solidity contracts

## 2. migrations/ folder
Contains the scriptable deployment files

## 3. build/contracts/ folder
Contains the deployed contracts (saved as json files) 

## 4. server/ folder

***server artifact***

**server.py**: acts as the backend of the Trainee's UI frontend

***testing artifacts***

Used only for **testing** purposes

**test_trainer.py**: acts as a trainer agent

**test_trainee.py**: acts as a trainee agent

**test_mlagents.py**: acts as a mlagents agent

**trainee.py**: defines the *trainee* class used by test_trainee.py

## 5. client/trainee folder

## 6. client/trainer forder

#### the 'truffle-config.js' file defines the necessary Truffle configuration 

# Truffle

## Installation of truffle
**npm install -g truffle**

## Useful commands
From a command prompt, navigate to 'truffle-training' folder.

**truffle console**

**compile** - compiles a modified smart contract

**migrate** - deploys *all* contracts

**deploy --reset -f 2 --to 2** - resets _only_ the 2nd contract (removes it from ganache) and re-deploys it

## Testing thru Truffle console

    var dm; Training.at("0x0e3D8e15019fBB71F45b619fA38c3e90D8C96045").then( function(x) { dm = x });

defines `dm` as an instance of the Training contract

    dm.trainer().then( function(x) { return x.toString(); });

prints the trainer address

    dm.traineeAddr().then( function(x) { return x.toString(); });

prints the trainee address

    var tk; TokenERC20.at("0x79091CB21cd0b7a19f909806C3683BCf599Cf6eE").then( function(x) { tk = x });

defines `tk` as an instance of the Token contract

    let accounts = await web3.eth.getAccounts()

`account` contains the list of valid accounts set up through Ganache

    tk.balanceOf(accounts[0]).then( function(x) { return x.toString(); });

lists the current balance of the 10th account specifies by Ganache

***testing process***

    dm.requestDemo("xxxx", 13, {from: accounts[9]})
    dm.sendRate(5, 4, {'from': accounts[0]})
    dm.sendDemo(5, 'QmQJFMHq6FopbfWJVkAppXYxm3jJYGH2QQmDuCJTZDBN49', {'from': accounts[0]})
    dm.trainingCompleted(5, 133, {from: accounts[9]})

    tk.approve("0x0e3D8e15019fBB71F45b619fA38c3e90D8C96045", 5320000, {from: accounts[9]})
    dm.safePay(5, 133, {'from': accounts[9]})


