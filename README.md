# GeHoleQubit-Simulator

GeHoleQubit-Simulator is a research-oriented Python framework for building transparent numerical models of germanium/silicon-germanium (Ge/SiGe) hole-spin qubits. The project is intended to sit between simple analytical models and full-scale commercial or multiphysics device simulation. Its purpose is not to hide the physics behind a single black-box command, but to make each modeling step explicit enough that a researcher can inspect the governing equations, verify the units, test numerical convergence, and understand which assumptions control the final prediction. The long-term objective is to create a coherent open research workflow that connects electrostatic confinement, orbital structure, spin response, electrical susceptibility, and decoherence in a form that is practical for device design and scientific interpretation.

The central scientific motivation comes from the strongly anisotropic nature of hole-spin qubits in strained Ge/SiGe heterostructures. Hole states can exhibit large and highly direction-dependent effective (g)-factors because the spin degree of freedom is entangled with orbital structure, confinement, strain, and spin-orbit coupling. As a consequence, the qubit transition frequency is not determined by a single scalar (g)-factor. Instead, it is naturally described using an effective (g)-tensor. At the same time, gate voltages that shape the confinement potential can modify that spin response, which means that electrical control and electrical noise are intrinsically linked. A realistic computational framework therefore has to treat magnetic-field orientation, orbital confinement, gate-voltage sensitivity, and dephasing as connected parts of the same problem.

At the current stage, the repository provides a set of validated low-level building blocks. These include effective Zeeman calculations based on a (3	imes3) (g)-tensor, conversion between spherical magnetic-field angles and Cartesian field vectors, principal-axis analysis of the tensor (G=g^Tg), simple one-dimensional effective-mass confinement, and first-order quasistatic dephasing models that support correlated electrical noise. These capabilities are intentionally modular. A user can study only the Zeeman response, only the confinement problem, or only the dephasing calculation, while still retaining the option to connect the pieces into a larger device workflow.

For a magnetic field (mathbf B), the effective Zeeman splitting is modeled as

[
Delta E_Z=mu_Bleft|mathbf gmathbf Bight|,
]

where (mu_B) is the Bohr magneton and (mathbf g) is the effective (g)-tensor. The corresponding qubit frequency is

[
f_Z=rac{Delta E_Z}{h}.
]

This form naturally captures anisotropy because the magnitude of (mathbf gmathbf B) depends on the field direction. The package also works with the symmetric tensor

[
G=g^Tg,
]

whose eigenvectors define principal magnetic-field directions and whose eigenvalues determine the squares of the principal effective (g)-factors. This representation is particularly useful because the observable Zeeman splitting depends on (G) even when the matrix representation of (g) itself is not unique under basis transformations.

The confinement module currently implements a finite-difference solution of the one-dimensional effective-mass Schrödinger equation,

[
left[
-rac{hbar^2}{2m^*}rac{d^2}{dx^2}
+
V(x)
ight]psi_n(x)
=
E_npsi_n(x).
]

The solver assumes a uniform spatial grid, a constant scalar effective mass, and Dirichlet boundary conditions. These assumptions are deliberately simple, but they are useful for validating the numerical infrastructure before moving to more realistic two-dimensional or multiband calculations. The repository includes a harmonic-oscillator benchmark so that the numerical level spacing can be compared against the analytical value (hbaromega). This kind of benchmark is important because a solver should be validated against a case with a known answer before it is trusted for less transparent device potentials.

The noise model focuses initially on quasistatic electrical fluctuations. If the qubit frequency depends on multiple gates, then a small fluctuation can be linearized as

[
delta f_Z
approx
sum_i
rac{partial f_Z}{partial V_i}delta V_i.
]

Writing the gate sensitivities as a vector (mathbf s) and the voltage-noise covariance as (mathbf C_V), the resulting frequency variance is

[
sigma_f^2=mathbf s^Tmathbf C_Vmathbf s.
]

This form is intentionally more general than assuming every gate fluctuates independently. Correlated voltage noise can be included through the off-diagonal elements of (mathbf C_V). For Gaussian quasistatic frequency noise, the Ramsey envelope convention used in this project is

[
W(t)=expleft[-2pi^2sigma_f^2t^2ight],
]

which gives the (1/e) dephasing time

[
T_2^*=rac{1}{sqrt{2}pisigma_f}.
]

The convention is stated explicitly because factors of (2), (pi), and definitions of one-sided versus two-sided spectral density are common sources of disagreement between different codes and publications.

The repository is organized as a Python package under `src/geholequbit`. The `core.py` module contains fundamental Zeeman and field-orientation utilities. The `gtensor.py` module contains principal-axis and effective-(g) analysis. The `confinement.py` module contains the current finite-difference Schrödinger solver and harmonic confinement helpers. The `noise.py` module implements covariance-based frequency-noise propagation and (T_2^*) calculations. The `examples` directory contains small runnable demonstrations, while the `tests` directory contains analytical and numerical validation checks. GitHub Actions automatically executes the test suite after repository updates so that regressions are detected early.

A typical installation uses an editable Python environment:

```bash
git clone https://github.com/premathul/GeHoleQubit-Simulator.git
cd GeHoleQubit-Simulator
python -m pip install -e .
```

For development, testing support can be installed with

```bash
python -m pip install -e .[dev]
pytest -q
```

A minimal Zeeman calculation can be written as

```python
import numpy as np
from geholequbit.core import field_from_angles, zeeman_frequency_hz

g = np.diag([0.25, 0.35, 8.0])
B = 0.5

for theta in (0, 30, 60, 90):
    field = field_from_angles(B, theta)
    frequency = zeeman_frequency_hz(g, field)
    print(theta, frequency / 1e9, "GHz")
```

The numerical values in this example are synthetic and are not intended to represent a calibrated experimental device. The purpose of the example is to demonstrate how an anisotropic tensor produces a strong angular dependence of the spin resonance.

The confinement solver can be exercised with a harmonic potential:

```python
import numpy as np
from geholequbit.confinement import harmonic_potential_ev, solve_1d_effective_mass

mass = 0.08
omega = 2 * np.pi * 100e9
x = np.linspace(-80e-9, 80e-9, 241)

V = harmonic_potential_ev(x, mass, omega)
energies, wavefunctions = solve_1d_effective_mass(
    x,
    V,
    effective_mass_m0=mass,
    n_states=4,
)

print(energies * 1e3)
```

The present code should be interpreted as a foundation rather than a complete device simulator. It does not yet perform self-consistent Poisson–Schrödinger calculations, does not solve a multiband Luttinger–Kohn Hamiltonian, and does not derive the (g)-tensor microscopically from strain, interfaces, or heavy-hole/light-hole mixing. It also does not yet compute realistic phonon-limited (T_1), electrically driven Rabi frequencies, orbital-dependent spin-orbit matrix elements, or experimentally calibrated lever arms. Those omissions are intentional and are documented rather than hidden. Any quantitative device prediction will ultimately require additional physical layers and comparison against experiment or a higher-fidelity solver.

The next major stage of development is to extend the confinement calculation from one dimension to two dimensions and eventually to realistic gate-defined potentials. That will require sparse-matrix methods, convergence studies with respect to mesh spacing and domain size, support for anisotropic or position-dependent effective mass, and a clean interface between electrostatic potential maps and the quantum solver. Once that infrastructure is stable, the project can begin incorporating more realistic hole physics, including heavy-hole/light-hole mixing, simplified Luttinger Hamiltonians, strain terms, and effective spin-orbit coupling.

A second major direction is to make the (g)-tensor itself a function of gate voltage and confinement. The physically relevant quantity for coherence is not only (g), but also derivatives such as

[
rac{partial g_{ij}}{partial V_k}
]

and therefore

[
rac{partial f_Z}{partial V_k}.
]

These quantities connect the microscopic device state to experimentally measurable dephasing. Once they are available, the simulator can interface directly with more detailed noise models, including (1/f) noise and filter-function calculations provided by the companion QuantumDot-Noise-Lab repository.

A third development direction is numerical uncertainty and convergence. A scientifically useful result should not consist only of a central value. The code should make it possible to quantify sensitivity to mesh spacing, effective-mass assumptions, fitted (g)-tensor elements, gate-noise amplitudes, and finite-difference step size. The long-term aim is for each major simulation to report both the predicted observable and the numerical or model uncertainty that accompanies it.

The project follows a reproducibility-first philosophy. A calculation should ideally record the model equations, numerical grid, constants, input parameters, solver tolerances, derivative step sizes, noise assumptions, software version, and Git commit. Future versions will increasingly use configuration files so that a complete calculation can be reproduced from a small version-controlled parameter set rather than from an undocumented notebook or interactive session.

The intended long-term workflow is

[
	ext{device geometry}
ightarrow
phi(mathbf r)
ightarrow
V(mathbf r)
ightarrow
psi_n(mathbf r)
ightarrow
g_{ij}
ightarrow
f_Z
ightarrow
rac{partial f_Z}{partial V_i}
ightarrow
T_2^*
ightarrow
T_1.
]

That roadmap is deliberately ambitious, but each intermediate stage is designed to remain independently testable. The project should remain useful even before the final end-to-end workflow is complete.

This repository is appropriate for exploratory calculations, numerical method development, graduate-level research training, analytical cross-checks, and reproducible comparisons with higher-fidelity semiconductor simulators. A result produced by this code should not be considered experimentally predictive solely because it is numerically precise. Physical calibration, convergence, model validity, and uncertainty analysis remain essential.

## Contact

**Athul Prem**

For questions, research discussion, collaboration, or suggestions related to this project, please contact Athul Prem through the GitHub account associated with this repository.
