import solver as slv
import numpy as np

n_0 = np.array([100, 100])
a = np.array([0.01, -0.01])
m = np.array([[0, 0],
			  [0, 0]])

time, res = slv.solve(n_0, a, m, 10, 0.1)
slv.draw(time, res, res.shape[0], time.shape[0])
