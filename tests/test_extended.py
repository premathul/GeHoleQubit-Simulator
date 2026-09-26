import numpy as np
from geholequbit.confinement import solve_1d_effective_mass, harmonic_potential_ev, HBAR_J_S, J_PER_EV
from geholequbit.gtensor import principal_g_values, effective_g
from geholequbit.noise import covariance_frequency_variance, gaussian_t2star_from_variance

def test_harmonic_spacing():
    m=0.08
    omega=2*np.pi*100e9
    x=np.linspace(-80e-9,80e-9,241)
    v=harmonic_potential_ev(x,m,omega)
    e,_=solve_1d_effective_mass(x,v,m,3)
    expected=HBAR_J_S*omega/J_PER_EV
    assert np.isclose(e[1]-e[0],expected,rtol=0.08)

def test_principal_g_diagonal():
    vals,_=principal_g_values(np.diag([1.,2.,3.]))
    assert np.allclose(vals,[3,2,1])
    assert np.isclose(effective_g(np.diag([1.,2.,3.]),[0,0,1]),3)

def test_correlated_noise():
    s=np.array([2.,3.])
    c=np.array([[4.,1.],[1.,9.]])
    var=covariance_frequency_variance(s,c)
    assert np.isclose(var,s@c@s)
    assert gaussian_t2star_from_variance(var)>0
