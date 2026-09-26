import numpy as np

def g_metric(g_tensor):
    """Return G = g^T g, the symmetric tensor controlling Zeeman magnitude."""
    g=np.asarray(g_tensor,float)
    if g.shape!=(3,3): raise ValueError("g_tensor must be 3x3")
    return g.T@g

def principal_g_values(g_tensor):
    """Principal effective-g values and corresponding field directions."""
    vals,vecs=np.linalg.eigh(g_metric(g_tensor))
    order=np.argsort(vals)[::-1]
    return np.sqrt(np.clip(vals[order],0,None)),vecs[:,order]

def effective_g(g_tensor, direction):
    n=np.asarray(direction,float)
    if n.shape!=(3,) or np.linalg.norm(n)==0:
        raise ValueError("direction must be a nonzero 3-vector")
    n=n/np.linalg.norm(n)
    return np.linalg.norm(np.asarray(g_tensor,float)@n)

def angular_map(g_tensor, theta_deg, phi_deg):
    out=np.empty((len(theta_deg),len(phi_deg)))
    for i,t in enumerate(theta_deg):
        for j,p in enumerate(phi_deg):
            tr,pr=np.deg2rad([t,p])
            n=[np.sin(tr)*np.cos(pr),np.sin(tr)*np.sin(pr),np.cos(tr)]
            out[i,j]=effective_g(g_tensor,n)
    return out
