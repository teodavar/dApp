# Scope
**A decentralized application that fully automates the workflow of the demonstrations’ trading and the Trainee agent training process**

![dapp Demo](demo/dapp-demo.gif)

# System decomposition
It contains of the following modules:

**Trainer software agent (TA):**
It is a mini web application that acts as an interface between Ethereum blockchain, Unity development platform and the IPFS decentralized file system. Through Unity development platform, Trainer software agent records the well-trained agent’s behaviour on a specific job into demo files. It then stores the recorded demonstration files into IPFS and interacts with smart contracts facilitating the demonstration’s trading process. 

**Trainee software agent (TEA):**

It is a mini web application that acts as an interface between Ethereum blockchain, ML-Agents RL platform, Unity and the IPFS decentralized file system. It interacts with Ethereum blockchains facilitating the demonstration files trading process. It retrieves the recorded demonstration files from IPFS and automatically requests from ML-Agents platform to initiate the training process.

**Two smart contracts:**

They are deployed and executed on the Ethereum blockchain. The NTUA Token (based on ERC 20 Token standard) is a custom token specifically created for research and experimentation purposes. The Training token maintains the demonstrations’ training process by carrying out and recording the relevant transactions. 

**Extended ML-Agents platform:**

The ML-Agents platform extended to support the initiation of the training process immediately after receiving a request from the Trainee software agent. It also periodically informs the Trainee software agent about the status of the training process (i.e., the reward gained at the end of each training session) and at the end of training it informs the Trainee SA of the mean reward gained during training.

**Unity development platform:**

Provides the complex environment that interacts with an agent during its training process providing feedback (reward or punishment) based on its own actions. It then records the trainer’s demonstration files. For conducting the experiments a new intelligent agent and its interacting environment was developed and deployed.

**IPFS:**

Physically stores the demonstration files. The Training smart contract only registers the demo’s IPFS hash address instead of the files

# Project structure
The project consists of the following git submodules:

**truffle-training**

Implements the the smart contracts and the trainer and trainee agents

**extended-ml-agents**

Implements the extention of the ML-agents platform

**Hummingbirds**

Implements the hummingbird intelligent agent and its interacting environment for conducting the experiments 
