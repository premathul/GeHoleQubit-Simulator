import numpy as np
from geholequbit.core import field_from_angles, zeeman_frequency_hz

g = np.diag([0.25, 0.35, 8.0])
B = 0.5
for theta in (0, 30, 60, 90):
    f = zeeman_frequency_hz(g, field_from_angles(B, theta))
    print(f"theta={theta:>3} deg  fZ={f/1e9:8.3f} GHz")
