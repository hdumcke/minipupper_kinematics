# Welcome to Minipupper Kinematics

## About this book

This book contains my notes and Jupyter notebooks that I created while gaining a better understanding of the kinematics of a quadruped robot in general and [MangDang Minipupper](https://github.com/mangdangroboticsclub/QuadrupedRobot) in particular.

We cover the mathematics for 2D and 3D movements and develop different gaits for the robot. The Jupyter notebooks contain the code that will illustrate the theoretical background. But theory and reality do not always match. We provide a simulation environment using the real-time physics simulation [pybullet](https://pybullet.org) and an execution environment that can be installed on a Minipupper so that we can upload leg trajectories to the physical robot and have them executed.

```{tableofcontents}
```

## A word of caution

This work is a product of my learning effort, not the product of an expert in the field. If I would write it again I would certainly to things differently. But I still hope if will be of use to the reader.

## How to install

### Installation of the development environment

The goal is to focus on portable Python code to be able to run it in any Python virtual environment. We make heavy use of [Jupyter Lab](https://blog.jupyter.org/~9b8906)

- Clone the repository
- Create a Python virtual environment
- cd into the jupyternb directory within this repository
- pip install -r requirements.txt
- start Jupyter lab with "jupyter lab ."

### Installation of the simulation environment

You must run in a Python virtual environment.

- cd into the controller directory within this repository
- run ./install.sh
- run "minipupper execute --help"

### Installation on Minipupper

Use a SD card that has been configured with [minipupper_base](https://github.com/hdumcke/minipupper_base)

- Clone this repository
- cd into the controller directory within this repository
- run ./install.sh
- minipupper walk # adjust parameters for your use case
