import json
import copy
from backend.controller.gaits3D import GaitController3D
from minipupper import CONF


class Wobble:

    def __init__(self, hardware_interface):
        self.hardware_interface = hardware_interface
        self.gc = GaitController3D()
        self.run = False
        self.isActive = False
        self.hasChanged = True
        self.params = {}
        self._setDefaults(self.params)

    def getAciveState(self):
        return self.isActive

    def _setDefaults(self, params):
        params['yaw'] = 0.
        params['pitch'] = 0.
        params['roll'] = 0.
        params['height'] = 0.

    def execute(self):
        if self.run:
            self._run()

    def _run(self):
        if not self.hasChanged:
            return
        lp = self.gc.getRPYH(self.params['roll'], self.params['pitch'], self.params['yaw'], self.params['height']/1000)
        for i in range(len(self.gc.legs)):
            if CONF.minipupper.environment == 'minipupper':
                lp[i][2] = lp[i][1] + lp[i][2]
            for j in range(len(self.gc.joints)):
                self.hardware_interface.set_servo_position(lp[i][j], j, i)
        self.hardware_interface.set_servo_position_done()
        self.hasChanged = False

    def start(self):
        if self.run:
            return
        self.run = True
        self._execute()

    def setParams(self, gait, command, param):
        self.current_gait = gait
        if command == 'status':
            self.run = param == 'start'
            if self.run:
                self.isActive = True
            else:
                self.isActive = False
                self._setDefaults(self.params)
                self.hasChanged = True
                self._run()
            return
        self.params[command] = float(param)
        self.hasChanged = True
        return

    def getParams(self, gait, command, param):
        ret = copy.deepcopy(self.params)
        if command == 'status':
            if param == 'stop':
                self._setDefaults(ret)
            return json.dumps(ret)
        else:
            # setParams is called async and this command has not been updated
            ret[command] = float(param)
        return json.dumps(ret)
