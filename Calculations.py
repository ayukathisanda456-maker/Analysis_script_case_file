import numpy as np

def retrieve_wall_shear_velocity(profiles, mu):
    y = profiles['y']
    u = profiles['rU']

    if y.size<2 or u.size <2:
        raise ValueError("Files too small to calculate the wall gradient")

    if y[1] == y[0]:
        raise ValueError("The first two coordinates are in-different")

    du_dy = (u[1] - u[0]) / (y[1] - y[0])

    return float(np.sqrt(mu*du_dy))


