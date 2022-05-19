import numpy as np
import daiquiri
from minipupper import CONF

logger = daiquiri.getLogger(__name__)


class LegController:

    def __init__(self):
        self.leg_names = {}
        self.servo_arm_length = CONF.servo_arm_length
        self.servo_delta_x = CONF.servo_delta_x
        self.servo_delta_y = CONF.servo_delta_y
        for leg in CONF.legs:
            self.leg_names[CONF.legs[leg]] = leg

    def less_then(self, a, b):
        if np.isclose(a, b):
            return False
        return a < b

    def greater_then(self, a, b):
        if np.isclose(a, b):
            return False
        return a > b

    def check_angles(self, leg, all_angles):
        fail_tests = False
        if self.less_then(all_angles[1] + all_angles[2], -np.pi/2):
            fail_tests = True
            logger.warn("Sum of angles exceeds minimum: leg = %s theta = %.5f gamma = %.5f" % (self.leg_names[leg], np.degrees(all_angles[1]), np.degrees(all_angles[2])))
        if self.greater_then(all_angles[1] + all_angles[2], 0):
            fail_tests = True
            logger.warn("Sum of angles exceeds maximum: leg = %s theta = %.5f gamma = %.5f" % (self.leg_names[leg], np.degrees(all_angles[1]), np.degrees(all_angles[2])))
        if self.greater_then(all_angles[1], -np.pi/2):
            fail_tests = True
            logger.warn("Theta exceeds maximum: leg = %s theta = %.5f gamma = %.5f" % (self.leg_names[leg], np.degrees(all_angles[1]), np.degrees(all_angles[2])))
        if self.less_then(all_angles[1], -np.pi):
            fail_tests = True
            logger.warn("Theta exceeds minimum: leg = %s theta = %.5f gamma = %.5f" % (self.leg_names[leg], np.degrees(all_angles[1]), np.degrees(all_angles[2])))
        if self.less_then(all_angles[2], np.pi/4):
            fail_tests = True
            logger.warn("Gamma exceeds minimum: leg = %s theta = %.5f gamma = %.5f" % (self.leg_names[leg], np.degrees(all_angles[1]), np.degrees(all_angles[2])))
        if self.greater_then(all_angles[2], 3*np.pi/4):
            fail_tests = True
            logger.warn("Gamma exceeds maximum: leg = %s theta = %.5f gamma = %.5f" % (self.leg_names[leg], np.degrees(all_angles[1]), np.degrees(all_angles[2])))

        return fail_tests

    def get_minipupper_servo_angle(self, all_angles):
        return all_angles[1] + all_angles[2]
