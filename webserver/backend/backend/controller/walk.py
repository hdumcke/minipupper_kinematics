import json
import copy
from backend.controller.gaits3D import GaitController3D
from minipupper import CONF
import time
import numpy as np


class Walk:

    def __init__(self, hardware_interface):
        self.hardware_interface = hardware_interface
        self.gc = GaitController3D()
        self.run = False
        self.update_gait_plan = False
        self.setToNeutral = False
        self.current_gait = ''
        self.gait_plan = [[], [], [], []]
        self.params = {'walk': {}, 'trot': {}, 'gallop': {}}
        for gait in self.params:
            self._setDefaults(self.params[gait])

    def _setDefaults(self, params):
        self.frequency = 1./120
        self.gc.step_length = 0.04
        self.gc.step_height = 0.01
        self.gc.number_of_points = 10
        params['vel_x'] = 0
        params['vel_y'] = 0
        params['frequency'] = 120
        params['step_length'] = 4
        params['step_height'] = 1
        params['number_of_points'] = 10

    def execute(self):
        if self.setToNeutral:
            self._setNeutral()
            self.setToNeutral = False
            return
        if not self.run:
            time.sleep(self.frequency)
            return
        if self.update_gait_plan:
            self._setGaitPlan()
            self.update_gait_plan = False
        self._run()

    def _setGaitPlan(self):
        angle = np.arctan2(self.params[self.current_gait]['vel_y'], self.params[self.current_gait]['vel_x'])
        speed = max(abs(self.params[self.current_gait]['vel_x']), abs(self.params[self.current_gait]['vel_y']))
        self.gait_plan = self.gc._gait_plan(angle, self.current_gait, speed)
        if CONF.minipupper.environment == 'minipupper':
            for k in range(len(self.gait_plan[0])):
                for i in range(len(self.gc.legs)):
                    self.gait_plan[i][k][2] = self.gait_plan[i][k][1] + self.gait_plan[i][k][2]

    def _run(self):
        for k in range(len(self.gait_plan[0])):
            for i in range(len(self.gc.legs)):
                for j in range(len(self.gc.joints)):
                    self.hardware_interface.set_servo_position(self.gait_plan[i][k][j], j, i)
            self.hardware_interface.set_servo_position_done()
            time.sleep(self.frequency)

    def _setNeutral(self):
        neutral = self.gc.mpInverseKinAllLegs(np.transpose(np.copy(self.gc.neutral_foot_position)))
        if CONF.minipupper.environment == 'minipupper':
            for i in range(len(self.gc.legs)):
                neutral[i][2] = neutral[i][1] + neutral[i][2]
        for i in range(len(self.gc.legs)):
            for j in range(len(self.gc.joints)):
                self.hardware_interface.set_servo_position(neutral[i][j], j, i)
        self.hardware_interface.set_servo_position_done()

    def setParams(self, gait, command, param):
        self.current_gait = gait
        if command == 'freq':
            self.params[self.current_gait]['frequency'] = float(param)
            self.frequency = 1./float(param)
            return
        if command == 'step_l':
            self.gc.step_length = float(param)/100
            self.params[self.current_gait]['step_length'] = float(param)
            self.update_gait_plan = True
            return
        if command == 'step_h':
            self.params[self.current_gait]['step_height'] = float(param)
            self.gc.step_height = float(param)/100
            self.update_gait_plan = True
            return
        if command == 'number_of_points':
            self.params[self.current_gait]['number_of_points'] = float(param)/100
            self.gc.number_of_points = int(param)
            self.update_gait_plan = True
            return
        if command == 'status':
            self.run = param == 'start'
            if not self.run:
                self._setDefaults(self.params[self.current_gait])
                self.setToNeutral = True
            else:
                self.update_gait_plan = True
            return
        self.params[gait][command] = float(param)
        self.update_gait_plan = True
        return

    def getParams(self, gait, command, param):
        ret = copy.deepcopy(self.params[gait])
        if command == 'status' and param == 'stop':
            self._setDefaults(ret)

        return json.dumps(ret)
