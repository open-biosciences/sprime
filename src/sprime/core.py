"""Core S′ / pS′ / ΔpS′ computations.

S′ = asinh( (E_max / EC50) * C_ref ), with C_ref a reference concentration (default 1 µM)
that non-dimensionalizes the E_max/EC50 ratio (standard practice, cf. Michaelis-Menten / Hill).

OPEN DEFINITION — E_max convention
----------------------------------
`emax_as_percent` controls whether E_max is supplied as a percent (0-100) or a fraction (0-1).
This choice sets the absolute S′ scale and therefore any fixed thresholds (e.g. +/-2, +/-4).
It MUST be reconciled with the reference SPrime implementation before release. The cohort S′
values reported in the lung study (~7-10) are consistent with the *percent* convention.
"""
from __future__ import annotations
import numpy as np


def s_prime(emax, ec50_uM, c_ref_uM: float = 1.0, emax_as_percent: bool = True):
    """Operational potency-efficacy index for a single compound-cell-line pair.

    Parameters
    ----------
    emax : float | array   E_max = upper - lower 4PL asymptote (percent if emax_as_percent).
    ec50_uM : float | array  EC50 in micromolar.
    c_ref_uM : float  reference concentration (default 1 µM) that cancels EC50 units.
    emax_as_percent : bool  see module docstring (OPEN definition).
    """
    emax = np.asarray(emax, dtype=float)
    ec50 = np.asarray(ec50_uM, dtype=float)
    e = emax if emax_as_percent else emax * 100.0   # normalize convention internally
    arg = (e / ec50) * (c_ref_uM / 1.0)
    return np.arcsinh(arg)


def pooled_ps(s_values):
    """pS′ = mean S′ across a cohort."""
    return float(np.mean(np.asarray(s_values, dtype=float)))


def delta_ps(s_wt, s_mut):
    """ΔpS′ = pS′_WT - pS′_mutant."""
    return pooled_ps(s_wt) - pooled_ps(s_mut)


def bootstrap_delta_ps_ci(s_wt, s_mut, n_boot: int = 1000, alpha: float = 0.05, seed: int | None = 0):
    """Nonparametric bootstrap 95% CI for ΔpS′ (resample each cohort with replacement)."""
    rng = np.random.default_rng(seed)
    s_wt = np.asarray(s_wt, dtype=float); s_mut = np.asarray(s_mut, dtype=float)
    draws = np.empty(n_boot)
    for i in range(n_boot):
        w = rng.choice(s_wt, size=s_wt.size, replace=True)
        m = rng.choice(s_mut, size=s_mut.size, replace=True)
        draws[i] = w.mean() - m.mean()
    lo, hi = np.percentile(draws, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(delta_ps(s_wt, s_mut)), float(lo), float(hi)
