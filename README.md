# Overview

This repositiorie contains Jupyter notebook that I used to gain a better understanding of the kinematics of a quadruped robot in generate and <a href="https://github.com/mangdangroboticsclub/QuadrupedRobot">MangDang Minipupper</a> in particular.

We cover the mathematics for 2D and 3D movements and develop different gaits for the robot. The Jupyter notebooks contain that will illustrate the theoretical background. But theory and reality do not always match. We provide an execution environment that can be installed on a Minipupper so that we can upload leg trajectories to th ephysical robot and have them executed.

# Content

- Kinematics and Inverse kinematics of a two link manipulator (robot leg in 2D)
- Some discussion of URDF (Unified Robot Description Format)
- 2D leg movement, simulated and exectuted in the physical robot
- Discussion of movement in 3D
- Kinematics and Inverse kinematics of a three link manipulator (robot leg in 3D)
- 3D leg movement, simulated and exectuted in the physical robot
- Simulation of physics. Gravity is a reality

## Installation of the development environmet

The goal is to focus on portable Python code to be able to run it in any Python virtual environment. We make heavy use of <a href="https://blog.jupyter.org/jupyterlab-is-ready-for-users-5a6f039b8906">Jupyer Lab</a>

- Clone this repository
- Create a Python virtual environment
- cd into the jupyternb directory within this repository
- pip install -r requirements.txt
- start Jupyter lab with "jupyter lab ."

### A note on Jupyter notebooks and Git

Since execution of a notebook will write updates to the file refrain from working on the main branch:

git checkout -b dev main

For more details checkout <a href="https://mg.readthedocs.io/git-jupyter.html">Jupyter Notebooks in a Git Repository</a>

## Installation of the simulation environmet

You must run in a Python virtual environment.

- cd into the controller directory within this repository
- run ./install.sh
- run "minipupper execute --help"

## Installation on Minipupper

Use a SD card that has been configured with  <a href="https://github.com/hdumcke/minipupper_base">minipupper_base</a>

- Clone this repository
- cd into the controller directory within this repository
- run ./install.sh
- minipupper execute -l 3 -t 0.5 # adjust parameters for your use case

## Develop your own feet trajectories

- create your jupyter notebook based on the examples in this repo. Write the joint angles to a file. Do this for all 12 joints.
- test in the simulation environment
- scp joint angle files to your minipupper. The directory where these files are expected can be configured in /etc/minipupper/minipupper.yaml

## To Do

- This is work in progress and not all modules are yet developed.
- So far we reduce foot movement to 2D, hips will not move. 3D will come next.

