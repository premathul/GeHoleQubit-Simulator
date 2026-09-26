# GeHoleQubit-Simulator

Open-source research toolkit for simplified modeling of Ge/SiGe hole-spin qubits.

## Scope
This repository develops transparent, testable building blocks for:
- anisotropic hole-spin g-tensors and Zeeman splittings,
- magnetic-field orientation sweeps,
- voltage-to-frequency susceptibility,
- simple quasistatic dephasing estimates,
- reusable numerical utilities for Ge/SiGe spin-qubit studies.

The current implementation is deliberately lightweight and does **not** replace a calibrated multiband k·p, Poisson–Schrodinger, or commercial TCAD calculation.

## Quick start
```bash
python -m pip install -e .
python examples/basic_zeeman_scan.py
pytest
```

## Physics
For a magnetic field \\(\mathbf B\\), the effective Zeeman splitting is
\\[
\Delta E_Z = \mu_B \lVert \mathbf g \mathbf B \rVert,
\\]
with frequency \\(f_Z=\Delta E_Z/h\\).

The package also includes first-order quasistatic dephasing estimates from voltage sensitivities \\(\partial f_Z/\partial V_i\\).

## Status
Early research software. Generic example parameters only; no unpublished device geometry or proprietary calibration data are included.

## License
MIT.
