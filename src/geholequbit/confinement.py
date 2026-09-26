import numpy as np

HBAR_J_S = 1.054571817e-34
M0_KG = 9.1093837139e-31
J_PER_EV = 1.602176634e-19

def solve_1d_effective_mass(x_m, potential_ev, effective_mass_m0, n_states=4):
    """Finite-difference 1D effective-mass Schrödinger solver.

    Dirichlet boundary conditions are imposed at the endpoints.
    Returns (energies_eV, wavefunctions), with each wavefunction normalized
    so integral |psi|^2 dx = 1.
    """
    x=np.asarray(x_m,float)
    v=np.asarray(potential_ev,float)
    if x.ndim!=1 or v.shape!=x.shape or x.size<5:
        raise ValueError("x and potential_ev must be matching 1D arrays with >=5 points")
    dx=np.diff(x)
    if not np.allclose(dx,dx[0],rtol=1e-6,atol=0):
        raise ValueError("uniform grid required")
    if effective_mass_m0<=0:
        raise ValueError("effective_mass_m0 must be positive")
    d=float(dx[0]); m=effective_mass_m0*M0_KG
    t=(HBAR_J_S**2/(2*m*d**2))/J_PER_EV
    vi=v[1:-1]
    n=vi.size
    h=np.diag(vi+2*t)+np.diag(np.full(n-1,-t),1)+np.diag(np.full(n-1,-t),-1)
    evals,evecs=np.linalg.eigh(h)
    k=min(int(n_states),n)
    evals=evals[:k]; evecs=evecs[:,:k]
    psi=np.zeros((x.size,k))
    psi[1:-1,:]=evecs
    norms=np.sqrt(np.trapezoid(np.abs(psi)**2,x,axis=0))
    psi/=norms
    return evals,psi

def harmonic_potential_ev(x_m, mass_m0, omega_rad_s):
    """Harmonic potential 1/2 m omega^2 x^2 in eV."""
    m=mass_m0*M0_KG
    return 0.5*m*omega_rad_s**2*np.asarray(x_m,float)**2/J_PER_EV
