# Overview

This repositories contains Jupyter notebook that I used to gain a better understanding of the kinematics of a quadruped robot in general and <a href="https://github.com/mangdangroboticsclub/QuadrupedRobot">MangDang Minipupper</a> in particular.

We cover the mathematics for 2D and 3D movements and develop different gaits for the robot. The Jupyter notebooks contain that will illustrate the theoretical background. But theory and reality do not always match. We provide an execution environment that can be installed on a Minipupper so that we can upload leg trajectories to the physical robot and have them executed.

# Content

- Kinematics and Inverse kinematics of a two link manipulator (robot leg in 2D)
- Some discussion of URDF (Unified Robot Description Format)
- 2D leg movement, simulated and executed in the physical robot
- Discussion of movement in 3D
- Kinematics and Inverse kinematics of a three link manipulator (robot leg in 3D)
- 3D leg movement, simulated and executed in the physical robot
- Robot pose
- Simulation of physics. Gravity is a reality

## Installation of the development environment

The goal is to focus on portable Python code to be able to run it in any Python virtual environment. We make heavy use of <a href="https://blog.jupyter.org/jupyterlab-is-ready-for-users-5a6f039b8906">Jupyter Lab</a>

- Clone this repository
- Create a Python virtual environment
- cd into the repository
- run "./install.sh"

### Use the development environment

- cd into the repository
- start Jupyter lab with "jupyter lab jupyternb"

### A note on Jupyter notebooks and Git

Since execution of a notebook will write updates to the file refrain from working on the main branch:

git checkout -b dev main

For more details checkout <a href="https://mg.readthedocs.io/git-jupyter.html">Jupyter Notebooks in a Git Repository</a>

### Use the simulation environment

- run "minipupper --help" for instructions on how to use this command
- run "web-controller" and point your browser at the URL shown on the screen

## Installation on Minipupper

Use a SD card that has been configured with  <a href="https://github.com/hdumcke/minipupper_base">minipupper_base</a> Use Ubuntu 22.04 as this is the only version we have tested with so far.

- Clone this repository
- cd into the repository
- run ./install.sh
- reboot
- point your web browser at http://xx.xx.xx.xx:8080 where xx.xx.xx.xx is the IP address of your minipupper

For development you can also:

- run "minipupper execute --help"
- run "minipupper walk" and adjust parameters for your use case

## To Do

- This is work in progress, we have to fine tune gait parameters and to develop a mode where we change gaits as a function of the velocity
- Compete the jupyter notebooks
- Integrate with ROS2
- Quadruped movement is still on-going research, there are many interesting issues to look at. This is open source and you can do your own research.

