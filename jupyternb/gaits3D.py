import numpy as np
import os
import bezier
from pytransform3d.urdf import UrdfTransformManager


class GaitController3D:

    def __init__(self):
        self.legs = ['rf', 'lf', 'rh', 'lh']
        self.joints = ['hip', 'upper_leg', 'lower_leg']
        self.tm = UrdfTransformManager()
        urdf_file = '../mini-pupper_description/urdf/mini-pupper_fixed.urdf'
        if not os.path.exists(urdf_file):
            if 'VIRTUAL_ENV' in os.environ:
                urdf_file = "%s/etc/minipupper/mini-pupper_fixed.urdf" % os.environ['VIRTUAL_ENV']
            else:
                urdf_file = "/etc/minipupper/mini-pupper_fixed.urdf"
        with open(urdf_file, "r") as f:
            self.tm.load_urdf(f.read(), package_dir='../')
        self.d = np.linalg.norm(self.tm.get_transform('lf_upper_leg_link', 'lf_hip_link')[:3, 3:4].reshape(3))
        self.lu = np.linalg.norm(self.tm.get_transform('lf_lower_leg_link', 'lf_upper_leg_link')[:3, 3:4].reshape(3))
        self.ll = np.linalg.norm(self.tm.get_transform('lf_foot_link', 'lf_lower_leg_link')[:3, 3:4].reshape(3))
        for leg in self.legs:
            for servo in self.joints:
                if 'hip' in servo:
                    angle = 0.0
                if 'upper' in servo:
                    angle = np.pi/4
                if 'lower' in servo:
                    angle = -np.pi/2
                self.tm.set_joint('%s_%s_joint' % (leg, servo), angle)
        self.neutral_foot_position = np.zeros((4, 3))
        for i in range(len(self.legs)):
            leg = self.legs[i]
            self.neutral_foot_position[i, :] = self.tm.get_transform('%s_foot_link' % leg, 'base_link')[:3, 3:4].reshape(3)

        self.step_length = 0.04
        self.step_height = 0.01
        self.velocity_adapt = 4
        self.number_of_points = 10

    def mpForwardKin(self, leg, angles):
        self.tm.set_joint('%s_hip_joint' % leg, angles[0])
        self.tm.set_joint('%s_upper_leg_joint' % leg, angles[1])
        self.tm.set_joint('%s_lower_leg_joint' % leg, angles[2])
        return self.tm.get_transform('%s_foot_link' % leg, 'base_link')[:3, 3:4].reshape(3)

    def mpInverseKin(self, leg, point):
        hip = self.tm.get_transform('%s_hip_link' % leg, 'base_link')[:3, 3:4].reshape(3)
        alpha = np.arctan2(point[2] - hip[2], point[1] - hip[1])
        r = np.linalg.norm([point[2] - hip[2], point[1] - hip[1]])
        beta = np.arctan2(self.d, np.sqrt(r**2-self.d**2))
        if 'r' in leg:
            beta = -beta
        phi = np.pi/2 + alpha - beta
        self.tm.set_joint('%s_hip_joint' % leg, phi)
        A = self.tm.get_transform('%s_hip_link' % leg, 'base_link')
        B = np.append(point, 1.)
        P = np.linalg.inv(A).dot(B)
        B = np.array([P[0], P[2]])
        gam = np.arccos(np.round((B[0]**2+B[1]**2-self.lu**2-self.ll**2)/(2*self.lu*self.ll), 10))
        A11 = self.lu + self.ll * np.cos(gam)
        A12 = -self.ll * np.sin(gam)
        A21 = self.ll * np.sin(gam)
        A22 = self.lu + self.ll * np.cos(gam)

        A = np.array([[A11, A12], [A21, A22]])
        X = np.linalg.inv(A).dot(B)
        thet = np.arctan2(X[1], X[0])
        return [phi, -(thet+np.pi/2), -gam]

    # ref: https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
    # using the Euler–Rodrigues formula https://en.wikipedia.org/wiki/Euler–Rodrigues_formula
    def _rotation_matrix(self, axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / np.sqrt(np.dot(axis, axis))
        a = np.cos(theta / 2.0)
        b, c, d = -axis * np.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    def mpInverseKinAllLegs(self, foot_pos):
        angles = np.zeros((4, 3))
        for i in range(len(self.legs)):
            angles[i] = self.mpInverseKin(self.legs[i], np.transpose(foot_pos)[i])
        return angles

    def getRPYH(self, roll, pitch, yaw, height):
        foot_pos = np.transpose(np.copy(self.neutral_foot_position))
        foot_pos[2] -= height
        foot_pos = np.dot(self._rotation_matrix([1, 0, 0], np.radians(roll)), foot_pos)
        foot_pos = np.dot(self._rotation_matrix([0, 1, 0], np.radians(-pitch)), foot_pos)
        foot_pos = np.dot(self._rotation_matrix([0, 0, 1], np.radians(yaw)), foot_pos)
        return self.mpInverseKinAllLegs(foot_pos)

    def _adjust_velocity(self):
        times = np.linspace(0, 1, num=self.number_of_points)
        return [((np.exp(self.velocity_adapt) + 1)/(np.exp(self.velocity_adapt) - 1))*(1/(np.exp(-2*self.velocity_adapt*(t-1/2))+1) - 1/(np.exp(self.velocity_adapt) + 1)) for t in times]

    def _stance_phase(self, speed, isWalking):
        save = self.number_of_points
        if isWalking:
            self.number_of_points = 3 * save
        self.number_of_points = int(self.number_of_points + int((100 - speed) / 2))
        v_adj = self._adjust_velocity()
        self.number_of_points = save
        return [self.step_length/2-x*self.step_length for x in v_adj]

    def _swing_phase(self):
        v_adj = self._adjust_velocity()
        bezier_points = np.asarray([
                                    [-self.step_length/2, 0.0, self.step_length/2, self.step_length/2],
                                    [0.0, self.step_height/0.75, self.step_height/0.75, 0.0]
                                   ])
        curve = bezier.Curve(bezier_points, degree=3)
        return curve.evaluate_multi(np.asarray(v_adj[1:-1]))

    def _trajectory(self, angle, speed, isWalking):
        stp = self._stance_phase(speed, isWalking)
        swp = self._swing_phase()
        traj_len = len(stp) + len(list(swp[0]))
        trajectory = np.zeros((traj_len, 3))
        trajectory[:, 0] = stp + list(swp[0])
        trajectory[:, 2][len(stp):] = list(swp[1])
        return np.transpose(np.dot(self._rotation_matrix([0, 0, 1], -angle), np.transpose(trajectory)))

    def _gait_plan(self, angle, gait, speed):
        feet_pos = [[], [], [], []]
        if speed == 0:
            return feet_pos
        isWalking = gait == 'walk'
        traj_front = self._trajectory(angle, speed, isWalking)
        traj_hind = self._trajectory(0, speed, isWalking)
        if gait == 'walk':
            gait_plan = [0, 1, 2, 3]
        if gait == 'trot':
            gait_plan = [0, 1, 1, 0]
        if gait == 'gallop':
            gait_plan = [0, 0, 1, 1]
        for leg in range(len(self.legs)):
            if leg < 2:
                traj = traj_front
            else:
                traj = traj_hind
            for tick in range(len(traj)):
                fp = self.mpInverseKin(self.legs[leg], self.neutral_foot_position[leg] + traj[tick])
                feet_pos[leg].append(fp)
            feet_pos[leg] = np.roll(feet_pos[leg], gait_plan[leg]*(self.number_of_points-2), axis=0)
        return feet_pos
