import socket
import copy
import pickle
import numpy as np
from backend.controller.gaits3D import GaitController3D


class Servo:

    def __init__(self, isServer=False):
        self.address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
        self.isServer = isServer
        self.bufferSize = 1024
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        if self.isServer:
            self.UDPSocket.bind(self.address)
            self.UDPSocket.setblocking(0)
        self.gc = GaitController3D()
        self.joint_pos = {}
        for leg in self.gc.legs:
            for joint in self.gc.joints:
                if joint == self.gc.joints[0]:
                    self.joint_pos["%s_%s" % (leg, joint)] = 0
                if joint == self.gc.joints[1]:
                    self.joint_pos["%s_%s" % (leg, joint)] = np.pi/4
                if joint == self.gc.joints[2]:
                    self.joint_pos["%s_%s" % (leg, joint)] = -np.pi/2

    def set_servo_position(self, angle, axis, leg):
        self.joint_pos["%s_%s" % (self.gc.legs[leg], self.gc.joints[axis])] = angle

    def set_servo_position_done(self):
        self.UDPSocket.sendto(pickle.dumps(self.joint_pos), self.address)

    def get_servo_positions(self):
        try:
            data, address = self.UDPSocket.recvfrom(self.bufferSize)
        except socket.error:
            pass
        else:
            self.joint_pos = copy.deepcopy(pickle.loads(data))
