import numpy as np
from geholequbit.core import zeeman_frequency_hz, t2star_quasistatic

def test_isotropic_frequency():
    f = zeeman_frequency_hz(np.eye(3)*2.0, [0,0,1.0])
    assert 27e9 < f < 29e9

def test_zero_noise_is_infinite():
    assert np.isinf(t2star_quasistatic([0.0], [1e-6]))
