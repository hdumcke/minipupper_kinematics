import numpy as np
import daiquiri
from minipupper import CONF

logger = daiquiri.getLogger(__name__)


class Servo:

    def __init__(self):
        self.leg_names = {}
        for leg in CONF.legs:
            self.leg_names[CONF.legs[leg]] = leg
        self.joint_names = {}
        for joint in CONF.joints:
            self.joint_names[CONF.joints[joint]] = joint
        # store joint positons
        self.joint_pos = {}
        for leg in CONF.legs:
            for joint in CONF.joints:
                self.joint_pos["%s_%s" % (leg, joint)] = 0

    def set_servo_position(self, angle, axis, leg):
        # Simulator uses an angle offset for the upper leg
        simulatorpupper_offset = 0
        if axis == 1:
            simulatorpupper_offset = -np.pi/2

        angle = angle - simulatorpupper_offset
        logger.debug("setting %s_%s to %.2f [degree]" % (self.leg_names[leg], self.joint_names[axis], np.degrees(angle)))
        self.joint_pos["%s_%s" % (self.leg_names[leg], self.joint_names[axis])] = angle
