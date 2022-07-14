import numpy as np
from gaits3D import GaitController3D


gc = GaitController3D()
phis = np.linspace(-np.pi/4, np.pi/4, 20)
thetas = np.linspace(-3*np.pi/4, -np.pi/4, 20)
gammas = np.linspace(0, np.pi/2, 20)

legs = ['lf', 'lh', 'rf', 'rh']
leg = 'rh'


def test_inverseKinematics(leg, phi, theta, gamma):
    theta = np.pi/4
    gamma = -np.pi/4
    P = gc.mpForwardKin(leg, [phi, theta, gamma])
    phi_cal, theta_calc, gamma_calc = gc.mpInverseKin(leg, P)

    np.testing.assert_almost_equal([phi, theta, gamma], [phi_cal, theta_calc, gamma_calc], decimal=5, err_msg='', verbose=True)

    np.testing.assert_almost_equal(P, gc.mpForwardKin(leg, [phi_cal, theta_calc, gamma_calc]), decimal=5, err_msg='', verbose=True)


for leg in legs:
    if 'l' in leg:
        orientation = 1
    else:
        orientation = -1
    for phi in phis:
        for theta in thetas[:-1]:
            for gamma in gammas:
                pass
                test_inverseKinematics(leg, orientation * phi, theta, gamma)

foot_pos = np.transpose(gc.neutral_foot_position)
leg = 0
# roll
res = np.dot(gc._rotation_matrix([1, 0, 0], np.radians(10)), foot_pos)
res1 = gc.getRPYH(10, 0, 0, 0)
res2 = gc.mpInverseKin(gc.legs[leg], np.transpose(res)[leg])
np.testing.assert_almost_equal(res1[leg], res2, decimal=5, err_msg='', verbose=True)
# pitch
res = np.dot(gc._rotation_matrix([0, 1, 0], np.radians(-10)), foot_pos)
res1 = gc.getRPYH(0, 10, 0, 0)
res2 = gc.mpInverseKin(gc.legs[leg], np.transpose(res)[leg])
np.testing.assert_almost_equal(res1[leg], res2, decimal=5, err_msg='', verbose=True)
# roll
res = np.dot(gc._rotation_matrix([0, 0, 1], np.radians(10)), foot_pos)
res1 = gc.getRPYH(0, 0, 10, 0)
res2 = gc.mpInverseKin(gc.legs[leg], np.transpose(res)[leg])
np.testing.assert_almost_equal(res1[leg], res2, decimal=5, err_msg='', verbose=True)
