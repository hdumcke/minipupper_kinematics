import numpy as np
import daiquiri
import pybullet as p
import time
import os
import pybullet_data
from minipupper import CONF

logger = daiquiri.getLogger(__name__)


class Simulator:

    def __init__(self,  hardware_interface):
        self.hardware_interface =  hardware_interface
        defaultERP = 0.4
        self.maxMotorForce = 5000
        maxGearForce = 10000
        jointFriction = 0.1
        dT = 0.005

        physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, False)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, False)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0,0,-10.)
        planeId = p.loadURDF("plane.urdf")
        startPos = [0,0,0.1]
        startOrientation = p.getQuaternionFromEuler([0,0,0])

        camTargetPos = [0., 0.7, -0.15]
        camDist = 1
        camYaw = 2
        camPitch = -16
        p.resetDebugVisualizerCamera(camDist, camYaw, camPitch, camTargetPos)
        p.setRealTimeSimulation(0)
        self.pupper = p.loadURDF("%s/etc/minipupper/minipupper.urdf" % os.environ['VIRTUAL_ENV'],
                            startPos, startOrientation) 

        jointTypeNames = {}
        jointTypeNames[p.JOINT_REVOLUTE] = "JOINT_REVOLUTE"
        jointTypeNames[p.JOINT_FIXED] = "JOINT_FIXED"

        self.jointNamesToIndex = {}

        for j in range(p.getNumJoints(self.pupper)):
          jointInfo = p.getJointInfo(self.pupper, j)
          jointInfoName = jointInfo[1].decode("utf-8")
          self.jointNamesToIndex[jointInfoName] = j
          p.setJointMotorControl2(self.pupper, j, p.VELOCITY_CONTROL, targetVelocity=0, force=jointFriction)

        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, True)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, True)

        #set the center of mass frame (loadURDF sets base link frame)  startPos/Orn
        p.resetBasePositionAndOrientation(self.pupper, startPos, startOrientation)


    def step(self):
        for f in self.hardware_interface.joint_pos.keys():
            p.setJointMotorControl2(self.pupper,
                                   self.jointNamesToIndex["%s_joint" % f],
                                   p.POSITION_CONTROL,
                                   targetPosition = self.hardware_interface.joint_pos[f],
                                   force = self.maxMotorForce)
        p.stepSimulation()

    def disconnect(self):
        p.disconnect()
