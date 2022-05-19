import numpy as np
from gaits import GaitController


gc = GaitController(1, 1, 1, 1, 1, 1)
thetas = np.linspace(-3*np.pi/4, -np.pi/4, 20)
gammas = np.linspace(0, np.pi/2, 20)
zmax = -1.2171440952799093


for theta in thetas[:-1]:
    for gamma in gammas:

#        if (theta + gamma) < zmax:
#            gamma = zmax - theta
#       print("theta = np.radians(%.5f) gamma = np.radians(%.5f)" % (np.degrees(theta), np.degrees(gamma)))
#        print("thetas = [%.10f] gammas = [%.10f]" % (theta, gamma))
#        np.testing.assert_array_less([zmax], [theta + gamma], err_msg='', verbose=True)

        P = gc.mpForwardKin([theta, gamma])[:,2]
        theta_calc, gamma_calc = gc.mpInverseKin(P)
#        print(P)
#        print("theta_calc = np.radians(%.5f) gamma_calc = np.radians(%.5f)" % (np.degrees(theta_calc), np.degrees(gamma_calc)))

        np.testing.assert_almost_equal([theta, gamma], [theta_calc, gamma_calc], decimal=5, err_msg='', verbose=True)

        np.testing.assert_almost_equal(P, gc.mpForwardKin([theta_calc, gamma_calc])[:,2], decimal=5, err_msg='', verbose=True)
