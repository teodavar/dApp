# **Modified release** of Unity ML-Agents Toolkit

**ML-Agent's release used is `Release 2`. Click
[here](https://github.com/Unity-Technologies/ml-agents/tree/release_2_docs/docs/Readme.md)
to get started with the latest release of ML-Agents.**

This project contains an extension of the Python API part of the ML-Agents in order to expose a new Rest endpoint (http://localhost:5100). Through this endpoint the Python API can automatically initiate a training session and inform the server part of the Trainee agent (http://localhost:5200) about the training progress.

## Example Unity environments

For the Thesis needs two (2) of the example Unity environments (https://github.com/Unity-Technologies/ml-agents/blob/release_2_docs/docs/Learning-Environment-Examples.md) are used:

### Crawler
**Set-up**: A creature with 4 arms and 4 forearms.

**Goal**: The agent must move its body toward the goal direction without falling.

CrawlerStaticTarget - Goal direction is always forward.

CrawlerDynamicTarget- Goal direction is randomized.

**Agent Reward Function** (independent):

*+0.03* times body velocity in the goal direction.

*+0.01* times body direction alignment with goal direction.

### Pyramids
**Set-up**: Environment where the agent needs to press a button to spawn a pyramid, then navigate to the pyramid, knock it over, and move to the gold brick at the top.

**Goal**: Move to the golden brick on top of the spawned pyramid.

**Agent Reward Function** (independent):

*+2* For moving to golden brick (minus *0.001* per step).


## Getting started

* Download and unzip the current project
* Install Unity 2019.3.15f1
* Launch Unity Hub
* On the Projects dialog, choose the Add option at the top of the window. Using the file dialog that opens, locate the Project folder and click Open.
* Install the com.unity.ml-agents as described in the https://github.com/Unity-Technologies/ml-agents/blob/release_2_docs/docs/Installation.md
* In the Project window, go to the Pyramids/Scenes folder and open the Pyramids scene file.

## Running a pre-trained model

* On the Hierarchy panel, navigate to Pyramids -> AreaPB -> Agent. In the Inspector panel - Behavior Parameters section, make sure that Model field contains the Pyramids (NN Model) file
* Click the Play button in the Unity Editor and you will see the agent trying to navigate to the pyramid, knock it over, and move to the gold brick at the top using the pre-trained model.

## ML-Agents Python API installation

1. Open an anaconda prompt terminal
2. Create an anaconda python environment: `conda create -n mlagents python=3.7`
3. Activate it: `conda activate mlagents`
4. Navigate to the current project folder
5. Install for development the mlagents python environment by running:
`pip install -e ./ml-agents-envs`
`pip install -e ./ml-agents`
6. To support the extentions made in the ML-agents Toolkit install the the following:
`pip install web3, Flask, flask-cors`

## Training a new model with Reinforcement Learning

7. Run:  `mlagents-learn ./config/gail_config.yaml --run-id=run_01`

where
*gail_config.yaml* is a training configuration file using BC, RL, GAIL and Curiocity learning techniques

*run-id* is a unique name for this training session.

* To resume a training run: `mlagents-learn ./config/gail_config.yaml --run-id=run_01 --resume` 

7. When the message "Start training by pressing the Play button in the Unity Editor" is displayed on the screen, you can press the Play button in Unity to start training in the Editor.