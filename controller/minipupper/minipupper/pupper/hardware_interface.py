from Mangdang.minipupper.HardwareInterface import HardwareInterface
import numpy as np
import daiquiri
from minipupper import CONF

logger = daiquiri.getLogger(__name__)


class Servo:

    def __init__(self):
        self.hardware_interface = HardwareInterface()
        self.leg_names = {}
        for leg in CONF.legs:
            self.leg_names[CONF.legs[leg]] = leg
        self.joint_names = {}
        for joint in CONF.joints:
            self.joint_names[CONF.joints[joint]] = joint

    def mp_angle(self, angle):
        return -np.pi/2 - angle

    def set_servo_position(self, angle, axis, leg, mp_angle):
        # Minipupper uses an angle offset for the upper leg
        if axis == 1:
            # we have to change lower leg servo
            self.hardware_interface.set_actuator_position(self.mp_angle(mp_angle), 2, leg)
            angle = self.mp_angle(angle)
        if axis == 2:
            angle = self.mp_angle(mp_angle)

        logger.debug("setting %s_%s to %.2f [degree]" % (self.leg_names[leg], self.joint_names[axis], np.degrees(angle)))
        self.hardware_interface.set_actuator_position(angle, axis, leg)
