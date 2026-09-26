# GeHoleQubit-Simulator

GeHoleQubit-Simulator is an open-source research software project for building transparent numerical models of **germanium/silicon-germanium (Ge/SiGe) hole-spin qubits**.

The long-term objective is to provide a modular workflow that connects semiconductor confinement physics to experimentally relevant qubit observables:

[
	ext{device potential}
ightarrow
	ext{orbital states}
ightarrow
g	ext{-tensor}
ightarrow
	ext{Zeeman splitting}
ightarrow
	ext{electrical susceptibility}
ightarrow
T_2^*
ightarrow
T_1.
]

The project is intentionally structured as a collection of small, auditable numerical components rather than as a black-box simulator. Each model is meant to expose its assumptions, units, approximations, and numerical conventions so that the calculation can be inspected and independently validated.

> **Important:** this repository is research software under active development. It does not currently replace a self-consistent Poisson–Schrödinger solver, multiband k·p package, QTCAD, COMSOL, or another calibrated device-level TCAD framework.

---

## 1. Scientific motivation

Hole-spin qubits in strained Ge/SiGe heterostructures are promising because they combine strong spin-orbit coupling, electrical controllability, low nuclear-spin environments, and compatibility with semiconductor nanofabrication.

These same advantages also make the physics highly anisotropic. The qubit frequency can depend strongly on:

- magnetic-field magnitude,
- magnetic-field orientation,
- confinement geometry,
- heavy-hole/light-hole mixing,
- gate voltages,
- vertical and lateral electric fields,
- strain,
- spin-orbit coupling,
- interface details,
- charge noise.

A useful modeling framework must therefore go beyond a single scalar (g)-factor or a single fitted coherence time.

This repository is being developed around that principle.

---

## 2. Current capabilities

The current codebase contains three main physics layers.

### 2.1 Effective Zeeman physics

For a magnetic field (mathbf B), the effective spin Hamiltonian can be written in terms of a (3	imes3) (g)-tensor,

[
H_Z = rac{mu_B}{2},oldsymbol{sigma}cdot mathbf g mathbf B.
]

The resulting Zeeman splitting is

[
Delta E_Z = mu_B left|mathbf gmathbf Bight|.
]

The corresponding qubit frequency is

[
f_Z = rac{Delta E_Z}{h}.
]

The package provides:

- conversion from magnetic-field angles to Cartesian vectors,
- Zeeman splitting in electronvolts,
- Zeeman frequency in hertz,
- effective (g)-factor evaluation,
- (g^Tg) metric construction,
- principal (g)-value extraction,
- principal magnetic-field directions,
- angular maps of (g_{m eff}).

### 2.2 One-dimensional effective-mass confinement

A finite-difference effective-mass Schrödinger solver is included as the first confinement layer.

For a particle with effective mass (m^*),

[
left[
-rac{hbar^2}{2m^*}rac{d^2}{dx^2}
+
V(x)
ight]psi_n(x)
=
E_npsi_n(x).
]

The numerical solver currently assumes:

- one spatial dimension,
- constant effective mass,
- uniform spatial grid,
- Dirichlet boundary conditions,
- scalar confinement potential,
- no explicit spin-orbit coupling.

It returns:

- low-lying eigenenergies,
- normalized eigenfunctions,
- orbital level spacings.

A harmonic-confinement utility is included for analytical benchmarking.

### 2.3 Quasistatic electrical dephasing

Suppose the qubit frequency depends on multiple gate voltages,

[
f_Z=f_Z(V_1,V_2,ldots,V_N).
]

To first order,

[
delta f
approx
sum_i
rac{partial f_Z}{partial V_i}delta V_i.
]

For a sensitivity vector

[
mathbf s =
left(
rac{partial f_Z}{partial V_1},
ldots,
rac{partial f_Z}{partial V_N}
ight),
]

and voltage-noise covariance matrix (mathbf C_V),

[
sigma_f^2
=
mathbf s^T mathbf C_V mathbf s.
]

For Gaussian quasistatic frequency noise, the Ramsey envelope convention used here is

[
W(t)
=
expleft[-2pi^2sigma_f^2t^2ight].
]

The corresponding (1/e) dephasing time is

[
T_2^*
=
rac{1}{sqrt{2}pisigma_f}.
]

The implementation supports both independent and correlated gate noise.

---

## 3. Repository structure

```text
GeHoleQubit-Simulator/
├── README.md
├── pyproject.toml
├── examples/
│   ├── example.py
│   └── confinement_demo.py
├── src/
│   └── geholequbit/
│       ├── __init__.py
│       ├── core.py
│       ├── confinement.py
│       ├── gtensor.py
│       └── noise.py
├── tests/
│   ├── test_core.py
│   └── test_extended.py
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 4. Installation

A recent Python installation is recommended.

```bash
git clone https://github.com/premathul/GeHoleQubit-Simulator.git
cd GeHoleQubit-Simulator
python -m pip install -e .
```

For development and testing:

```bash
python -m pip install -e .[dev]
pytest -q
```

---

## 5. Quick example: Zeeman anisotropy

```python
import numpy as np
from geholequbit.core import field_from_angles, zeeman_frequency_hz

g = np.diag([0.25, 0.35, 8.0])
B = 0.5

for theta in (0, 30, 60, 90):
    field = field_from_angles(B, theta)
    f = zeeman_frequency_hz(g, field)
    print(theta, f / 1e9, "GHz")
```

This is a synthetic example and is **not** intended to represent a calibrated device.

---

## 6. Quick example: confinement

```python
import numpy as np
from geholequbit.confinement import (
    harmonic_potential_ev,
    solve_1d_effective_mass,
)

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

The result can be compared with the analytical harmonic-oscillator spacing

[
E_{n+1}-E_n=hbaromega.
]

That comparison is included in the automated tests.

---

## 7. Numerical validation

The project uses explicit validation tests wherever possible.

Current checks include:

- isotropic (g)-tensor Zeeman frequency,
- principal-axis recovery for diagonal (g)-tensors,
- normalization of wavefunctions,
- harmonic oscillator level-spacing consistency,
- covariance-based frequency-noise propagation,
- correct zero-noise behavior for (T_2^*).

GitHub Actions automatically runs the test suite after pushes and pull requests.

Validation is treated as part of the scientific model, not merely as software maintenance.

---

## 8. Units and conventions

The project currently uses:

- magnetic field: tesla,
- energy: electronvolts unless a function explicitly states otherwise,
- frequency: hertz,
- position: meters,
- voltage: volts,
- time: seconds,
- effective mass: units of free-electron mass (m_0).

Every new public function should document its units.

Unit ambiguity is considered a bug.

---

## 9. What this project does not yet model

The current code does **not** yet provide:

- self-consistent electrostatics,
- realistic 2D or 3D gate geometry,
- spatially varying dielectric constants,
- multiband Luttinger–Kohn Hamiltonians,
- heavy-hole/light-hole mixing from first principles,
- Rashba or Dresselhaus terms from a microscopic Hamiltonian,
- strain-dependent band edges,
- atomistic interfaces,
- valley physics,
- realistic phonon-induced (T_1),
- calibrated device-specific voltage lever arms,
- finite-temperature occupation,
- many-body interactions.

These are roadmap items rather than hidden assumptions.

---

## 10. Planned development

### Phase I — effective models

- expand (g)-tensor utilities,
- voltage derivatives of the (g)-tensor,
- uncertainty propagation,
- arbitrary covariance matrices,
- field-angle sweeps,
- plotting utilities,
- structured parameter files.

### Phase II — confinement

- 2D finite-difference Schrödinger solver,
- anisotropic effective masses,
- position-dependent masses,
- double-well confinement,
- expectation values,
- orbital dipole matrix elements,
- mesh-convergence tools.

### Phase III — semiconductor-specific physics

- simplified Luttinger Hamiltonian,
- heavy-hole/light-hole mixing,
- strain terms,
- spin-orbit coupling,
- electric-dipole spin resonance observables,
- effective (g)-tensor extraction.

### Phase IV — coherence

- gate-specific susceptibility,
- correlated voltage noise,
- numerical (1/f) Ramsey envelopes,
- echo and dynamical-decoupling filters,
- (T_2^*) angular maps,
- phonon-assisted (T_1).

### Phase V — device-level workflow

The long-term architecture is

[
	ext{geometry}
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
partial f_Z/partial V_i
ightarrow
T_2^*,T_1.
]

---

## 11. Reproducibility philosophy

A scientific result should ideally contain enough information to reconstruct:

- model equations,
- numerical grid,
- physical constants,
- parameter values,
- solver tolerances,
- convergence criteria,
- random seeds,
- software version.

Future releases will move increasingly toward configuration-driven simulations so complete numerical experiments can be recreated from version-controlled parameter files.

---

## 12. Research use

The repository is intended for:

- exploratory calculations,
- method development,
- teaching,
- numerical verification,
- comparison against higher-fidelity solvers,
- reproducible research workflows.

A prediction should not be considered experimentally quantitative simply because the code returns many digits.

Model validity, convergence, calibration, and uncertainty must be established separately.

---

## 13. Contributing

Useful contributions include:

- physics-model implementations,
- analytical benchmark tests,
- numerical convergence tests,
- documentation improvements,
- bug reports,
- additional confinement models,
- plotting utilities,
- literature-backed physical constants.

New physics modules should preferably include:

1. the governing equation,
2. assumptions,
3. units,
4. at least one validation test,
5. a minimal example.

---

## 14. Citation

A formal `CITATION.cff` file will be added as the project matures.

Until then, if this repository contributes to academic work, cite the repository URL and the exact Git commit used in the calculation.

---

## 15. License

MIT License.

---

## 16. Project status

**Status:** active development.

The repository currently provides a validated foundation for effective Zeeman physics, simple confinement calculations, (g)-tensor analysis, and first-order quasistatic dephasing.

The scientific ambition is larger: to progressively connect Ge/SiGe device geometry to experimentally measurable spin-qubit coherence in a transparent, reproducible numerical framework.
