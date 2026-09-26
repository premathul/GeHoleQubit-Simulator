import numpy as np
from geholequbit.confinement import solve_1d_effective_mass, harmonic_potential_ev

mass=0.08
omega=2*np.pi*100e9
x=np.linspace(-80e-9,80e-9,241)
v=harmonic_potential_ev(x,mass,omega)
energies,_=solve_1d_effective_mass(x,v,mass,4)
print("Lowest orbital energies [meV]:")
for i,e in enumerate(energies):
    print(i, e*1e3)
