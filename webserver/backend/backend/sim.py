import time
from minipupper import CONF

if CONF.minipupper.environment == 'simulator':
    from backend.controller.simulator.pybullet import Simulator
    from backend.controller.simulator.hardware_interface import Servo


def main():
    if CONF.minipupper.environment == 'simulator':
        servo = Servo(isServer=True)
        sim = Simulator(servo)
        while True:
            servo.get_servo_positions()
            sim.step()
            time.sleep(1./240.)


if __name__ == "__main__":
    main()
