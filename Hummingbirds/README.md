# Hummingbirds

Based on https://learn.unity.com/course/ml-agents-hummingbirds

## Description

**Set-up**: A bird that moves towards flowers, dips in his beak and drinks nectar.

**Goal**: Agent must drink nectar as much as possible.

**Agents**: The environment contains one agent - bird.

**Agent Reward Function**:

**+0.01** per timestep (every .02 seconds, or 50x per second) while the bird dips his beak in the flower

**-0.5** each time the bird collides with the island boundaries

**Behavior Parameters**:
Possible actions: 
a) The bird can move forward, backward, right, left, up and down
b) The bird can pitch its head up and down (pitch angle)
c) The bird can turn its head right and left (yaw angle)

Possible observations:
a) Observe the bird's rotation
b) Get the distance from the beak tip to the nearest flower
c) Get the distance to the nearest flower
d) Observe whether the beak tip is in front of the flower 
e) Observe  whether the beak is pointing toward the flower

**Benchmark Mean Reward**: The bird drinks nectar from ~49 flower per training step (~35sec)

### Scenes
Four different (4) scenes are avaliable:
* `OneFlower`: a floating island with one flower
* `ClusterFlowers`: a floating island with only one small cluster of flowers
* `HiddenFlowers`: a floating island with cluster of flowers hidden between rocks and bushes
* `Training`: an floating island with a tree, rocks, bushes and several clusters of flowers


## Getting started

* Install Unity 2019.3.15f1
* Launch Unity Hub
* On the Projects dialog, choose the Add option at the top of the window.Using the file dialog that opens, locate the Hummingbirds folder  and click Open.
* Install the ml-agents Unity package: From Window menu, click on Package Manager -> Advanced -> Show Preview Packages, find MLAgents package (Version 1.0.2) and install it
* In the Project window, go to the Assets/Hummingbird/Scenes folder and open the Training scene file.

## Running a pre-trained model

* On the Hierarchy panel, navigate to FloatingIsland -> Hummingbird. In the Inspector panel - Behavior Parameters section, make sure that Model field contains the Hummingbrid04.nn file
* Click the Play button in the Unity Editor and you will see the hummingbird agent to move towards the flowers and drink the nectar using the pre-trained model.

## Training a new model with Reinforcement Learning

1. Open an anaconda prompt terminal
2. Create an anaconda python environment: `conda create -n humming python=3.7`
3. Activate it: `conda activate humming`
4. Install mlagents python environment: `pip3 install mlagents`
5. Navigate to the current project folder
6. Run:  `mlagents-learn ./config/trainer_config_04.yaml --run-id=run_01`

where
*trainer_config_04.yaml* is a training configuration file

*run-id* is a unique name for this training session.

* To resume a training run: `mlagents-learn ./config/trainer_config_04.yaml --run-id=run_01 --resume` 

7. When the message "Start training by pressing the Play button in the Unity Editor" is displayed on the screen, you can press the Play button in Unity to start training in the Editor.

