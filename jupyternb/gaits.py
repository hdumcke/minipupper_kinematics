import numpy as np
import bezier


class GaitController:

    def __init__(self,
                 step_length,
                 step_height,
                 velocity_adapt,
                 number_of_points,
                 theta,
                 gamma):
        self.step_length = step_length
        self.step_height = step_height
        self.velocity_adapt = velocity_adapt
        self.number_of_points = number_of_points
        self.theta = theta
        self.gamma = gamma
        self.bezier_points = np.asarray([
                                         [-self.step_length/2, 0.0, self.step_length/2, self.step_length/2],
                                         [0.0, self.step_height/0.75, self.step_height/0.75, 0.0]
                                        ])
        self.v_adj = np.array(self._adjust_velocity())
        self.stance_phase = np.zeros((2, number_of_points))
        self.stance_phase[0] = self._stance_phase()
        self.swing_phase = self._swing_phase()
        self.trajectory = np.concatenate((self.stance_phase, self.swing_phase), axis=1)
        self.lu = 0.05022511821787979  # from urdf
        self.ll = 0.065                # measured, includes the rubber foot

    def _adjust_velocity(self):
        times = np.linspace(0, 1, num=self.number_of_points)
        return [((np.exp(self.velocity_adapt) + 1)/(np.exp(self.velocity_adapt) - 1))*(1/(np.exp(-2*self.velocity_adapt*(t-1/2))+1) - 1/(np.exp(self.velocity_adapt) + 1)) for t in times]

    def _stance_phase(self):
        return self.step_length/2 - self.step_length * self.v_adj

    def _swing_phase(self):
        curve = bezier.Curve(self.bezier_points, degree=3)
        #return curve.evaluate_multi(np.ascontiguousarray(np.flip(self.v_adj[1:-1])))
        return curve.evaluate_multi(self.v_adj[1:-1])

    def get_trajectory(self):
        # translate to foot coordinate system and get servo positions
        t_vector = self.mpForwardKin([self.theta, self.gamma])[:, 2]
        self.trajectory_mp = np.empty(self.trajectory.shape)
        self.trajectory_mp[0] = self.trajectory[0] + t_vector[0]
        self.trajectory_mp[1] = self.trajectory[1] + t_vector[1]
        return self.trajectory_mp

    def get_bezier_points(self):
        # translate to foot coordinate system and get servo positions
        t_vector = self.mpForwardKin([self.theta, self.gamma])[:, 2]
        bezier_points = np.empty(self.bezier_points.shape)
        bezier_points[0] = self.bezier_points[0] + t_vector[0]
        bezier_points[1] = self.bezier_points[1] + t_vector[1]
        return bezier_points

    def _transformationMatrix(self, angle, length):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c, -s, length*c], [s, c, length*s], [0, 0, 1]])

    def mpForwardKin(self, angles):
        T1 = self._transformationMatrix(angles[0], self.lu)
        T2 = self._transformationMatrix(angles[1], self.ll)
        T3 = T1.dot(T2)
        P1 = T1.dot(np.array([0, 0, 1]))[0:2]
        P2 = T3.dot(np.array([0, 0, 1]))[0:2]
        return np.array([[0, P1[0], P2[0]], [0, P1[1], P2[1]]])

    def mpInverseKin(self, point):
        gam = np.arccos(np.round((point[0]**2+point[1]**2-self.lu**2-self.ll**2)/(2*self.lu*self.ll), 10))
        B = np.array(point)
        A11 = self.lu + self.ll * np.cos(gam)
        A12 = -self.ll * np.sin(gam)
        A21 = self.ll * np.sin(gam)
        A22 = self.lu + self.ll * np.cos(gam)

        A = np.array([[A11, A12], [A21, A22]])
        X = np.linalg.inv(A).dot(B)
        thet = np.arctan(X[1]/X[0])
        # correction for 3nd and 4rd quadrant
        # we assume -np.pi/4 < thet <= -3*np.pi/4
        if thet > -np.pi/4:
            thet = thet - np.pi
        return [thet, gam]

    def get_leg_servo_positions(self, shift=False):
        sp =  np.array([self.mpInverseKin([self.trajectory_mp[0][i], self.trajectory_mp[1][i]]) for i in range(len(self.trajectory_mp[0]))])
        if shift:
            return np.roll(sp, self.number_of_points, axis=0)
        else:
            return sp
