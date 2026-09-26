import numpy as np

def covariance_frequency_variance(sensitivities_hz_per_v, covariance_v2):
    """sigma_f^2 = s^T C s, retaining correlated gate noise."""
    s=np.asarray(sensitivities_hz_per_v,float)
    c=np.asarray(covariance_v2,float)
    if c.shape!=(s.size,s.size):
        raise ValueError("covariance shape must match number of sensitivities")
    var=float(s@c@s)
    if var < -1e-12:
        raise ValueError("covariance produced negative variance")
    return max(var,0.0)

def gaussian_t2star_from_variance(variance_hz2):
    """1/e Ramsey time for W=exp(-2*pi^2*sigma_f^2*t^2)."""
    if variance_hz2<0: raise ValueError("variance must be nonnegative")
    return np.inf if variance_hz2==0 else 1/(np.sqrt(2)*np.pi*np.sqrt(variance_hz2))

def gate_contributions(sensitivities_hz_per_v, sigma_v):
    s=np.asarray(sensitivities_hz_per_v,float)
    sig=np.broadcast_to(np.asarray(sigma_v,float),s.shape)
    return (s*sig)**2
