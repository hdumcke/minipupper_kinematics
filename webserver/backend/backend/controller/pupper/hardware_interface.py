from Mangdang.minipupper.HardwareInterface import HardwareInterface


class Servo:

    def __init__(self):
        self.hardware_interface = HardwareInterface()

    def set_servo_position(self, angle, axis, leg):
        self.hardware_interface.set_actuator_position(angle, axis, leg)

    def set_servo_position_done(self):
        pass
