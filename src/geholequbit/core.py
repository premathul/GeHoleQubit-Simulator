import numpy as np

MU_B_EV_T = 5.7883817982e-5
H_EV_S = 4.135667696e-15

def zeeman_splitting_ev(g_tensor, B):
    """Return effective Zeeman splitting in eV for tensor g and field B [T]."""
    g = np.asarray(g_tensor, dtype=float)
    b = np.asarray(B, dtype=float)
    if g.shape != (3, 3) or b.shape != (3,):
        raise ValueError("g_tensor must be 3x3 and B must have length 3")
    return MU_B_EV_T * np.linalg.norm(g @ b)

def zeeman_frequency_hz(g_tensor, B):
    return zeeman_splitting_ev(g_tensor, B) / H_EV_S

def field_from_angles(B_t, theta_deg, phi_deg=0.0):
    th, ph = np.deg2rad([theta_deg, phi_deg])
    return B_t * np.array([np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th)])

def t2star_quasistatic(sensitivities_hz_per_v, sigma_v):
    """Gaussian quasistatic T2* with W=exp[-2*pi^2*sigma_f^2*t^2]."""
    s = np.asarray(sensitivities_hz_per_v, float)
    sig = np.broadcast_to(np.asarray(sigma_v, float), s.shape)
    sigma_f = np.sqrt(np.sum((s*sig)**2))
    return np.inf if sigma_f == 0 else 1.0/(np.sqrt(2.0)*np.pi*sigma_f)
