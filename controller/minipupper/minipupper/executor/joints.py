import daiquiri
import time
import numpy as np

from minipupper import CONF

if CONF.minipupper.environment == 'simulator':
    from minipupper.simulator.hardware_interface import Servo
    from minipupper.simulator.pybullet import Simulator
else:
    from minipupper.pupper.hardware_interface import Servo

logger = daiquiri.getLogger(__name__)


class Reader:

    def __init__(self):
        self.servos_dir = CONF.minipupper.servos_dir
        logger.info("Reading from %s" % self.servos_dir)
        self.legs = CONF.legs
        self.joints = CONF.joints

    def read(self):
        movement = {}
        self.max_steps = 0

        for leg in self.legs.keys():
            for joint in self.joints.keys():
                name = "%s_%s" % (leg, joint)
                fn = "%s/%s" % (self.servos_dir, name)
                movement[name] = []
                with open("%s" % fn, 'r') as f:
                    for line in f:
                        movement[name].append(float(line.rstrip()))
                        self.max_steps = max(self.max_steps, len(movement[name]))

        self.angles = np.empty([4, 3, self.max_steps])

        for leg in self.legs.keys():
            for joint in self.joints.keys():
                name = "%s_%s" % (leg, joint)
                for step in range(self.max_steps):
                    self.angles[self.legs[leg]][self.joints[joint]][step] = movement[name][step % len(movement[name])]

    def get_max_steps(self):
        return self.max_steps

    def get_angles(self):
        return self.angles


class Servos:

    def __init__(self, angles):
        self.angles = angles
        self.hardware_interface = Servo()
        if CONF.minipupper.environment == 'simulator':
            self.simulator = Simulator(self.hardware_interface)

    def execute_loops(self, loops, step_duration, num_steps):
        self.loops = loops
        self.step_duration = step_duration
        while self.loops > 0:
            for i in range(num_steps):
                self.do_step(i)

            self.loops = self.loops - 1

        if CONF.minipupper.environment == 'simulator':
            self.simulator.disconnect

    def do_step(self, this_step):
        # check what has changed
        if this_step > 0:
            change_joints = self.angles[:, :, this_step] != self.angles[:, :, this_step-1]
        else:
            change_joints = np.full((4, 3), True)

        self._update_joints(self.angles[:, :, this_step], change_joints)

    def _update_joints(self, angles, change_joints):
        it = np.nditer(change_joints, flags=['f_index'])
        joints_to_update = []
        for x in it:
            if x:
                leg = it.index % 4
                axis = (it.index - 4*leg) % 3
                joints_to_update.append({'axis': axis,
                                         'leg': leg,
                                         'angle': angles[leg][axis]
                                        })

        self._set_servos(joints_to_update)

    def _set_servos(self, joints_to_update):
        for joint in joints_to_update:
            self.hardware_interface.set_servo_position(joint['angle'], joint['axis'], joint['leg'])

        #TODO This is not real time programming
        if CONF.minipupper.environment == 'simulator':
            if self.step_duration > (1./240.):
                sim_steps = self.step_duration/(1./240.)
                sim_loops = int(sim_steps)
                sim_remain = self.step_duration - sim_loops*(1./240.)
                while sim_loops:
                    self.simulator.step()
                    time.sleep(1./240.)
                    sim_loops = sim_loops -1
                time.sleep(sim_remain)
            else:
                self.simulator.step()
        else:
            time.sleep(self.step_duration)
