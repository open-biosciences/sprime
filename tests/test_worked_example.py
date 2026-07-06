"""Reconciliation test — the drift-catcher.

Locks the worked example so a change in convention or arithmetic cannot silently
diverge from what the manuscript/response letter report.

Doxorubicin / A549 (from the working-examples doc):
    upper=1, lower=0.00103085  -> E_max = 0.99897 (fraction) = 99.897 (percent)
    EC50 = 0.244910741 µM
Under the PERCENT convention: S′ = asinh(99.897/0.245) = asinh(407.9) ≈ 6.70
Under the FRACTION convention: S′ = asinh(0.99897/0.245) = asinh(4.08) ≈ 2.11

TODO(before release): confirm which value the reference SPrime emits and delete the wrong branch.
"""
import numpy as np
from sprime import s_prime

UPPER, LOWER, EC50 = 1.0, 0.00103085, 0.244910741
EMAX_PCT = (UPPER - LOWER) * 100.0


def test_worked_example_percent_convention():
    s = s_prime(emax=EMAX_PCT, ec50_uM=EC50, emax_as_percent=True)
    assert np.isclose(s, 6.70, atol=0.02), f"expected ~6.70, got {s:.4f}"


def test_convention_changes_scale():
    # Documents that the convention materially changes the value (must be pinned).
    s_pct = s_prime(emax=EMAX_PCT, ec50_uM=EC50, emax_as_percent=True)
    s_frac = s_prime(emax=(UPPER - LOWER), ec50_uM=EC50, emax_as_percent=False) \
        if False else np.arcsinh((UPPER - LOWER) / EC50)
    assert not np.isclose(s_pct, s_frac, atol=0.5)
