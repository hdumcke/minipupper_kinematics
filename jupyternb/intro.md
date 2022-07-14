# Welcome to Minipupper Kinematics

## About this book

This book contains my notes and Jupyter notebooks that I created while gaining a better understanding of the kinematics of a quadruped robot in general and [MangDang Minipupper](https://www.mangdang.net) in particular.

We cover the mathematics for 2D and 3D movements and develop different gaits for the robot. The Jupyter notebooks contain the code that will illustrate the theoretical background. But theory and reality do not always match. We provide a simulation environment using the real-time physics simulation [pybullet](https://pybullet.org) and an execution environment that can be installed on a Minipupper so that we can upload leg trajectories to the physical robot and have them executed. We also provide a web-based controller so that we can control the simulated or physical Minipupper from any web browser including a smartphone.

```{tableofcontents}
```

## A word of caution

This work is a product of my learning effort, not the product of an expert in the field. If I would write it again I would certainly to things differently. But I still hope if will be of use to the reader.

## How to install

### Installation on a PC

The goal is to focus on portable Python code to be able to run it in any Python virtual environment. We make heavy use of [Jupyter Lab](https://blog.jupyter.org/~9b8906)

- Clone the repository
- Create a Python virtual environment
- cd into the repository
- run "./install.sh"

### Use the development environment

- cd into the repository
- start Jupyter lab with "jupyter lab jupyternb"

### Use the simulation environment

- run "minipupper --help" for instructions on how to use this command
- run "web-controller" and point your browser at the URL shown on the screen


### Installation on Minipupper

Use a SD card that has been configured with [minipupper_base](https://github.com/hdumcke/minipupper_base) Use Ubuntu 22.04 as this is the only version we have tested with so far.

- Clone this repository
- cd into the repository
- run ./install.sh
- reboot
- point your web browser at http://xx.xx.xx.xx:8080 where xx.xx.xx.xx is the IP address of your minipupper

For development your can also:

- run "minipupper execute --help"
- run "minipupper walk" and adjust parameters for your use case
