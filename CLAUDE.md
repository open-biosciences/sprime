# CLAUDE.md — sprime

Orientation for a Claude Code session in this repo.

## What this is
`sprime` is the **reusable method module** behind the S′ (S-prime) potency–efficacy index:
a direction-preserving, variance-stabilized index over 4PL dose–response fits, plus its
cohort (`pS′`) and genotype-contrast (`ΔpS′`) forms.

    S′  = asinh( (E_max / EC50) × C_ref )   # C_ref = 1 µM
    pS′ = mean_i S′_i
    ΔpS′ = pS′_WT − pS′_mutant

It is the single source of truth for the math. The companion repo `sprime-lung-sl`
imports this module so the paper's numbers can't drift from the method.

## Layout
- `src/sprime/core.py` — `s_prime`, `pooled_ps`, `delta_ps`, `bootstrap_delta_ps_ci`
- `tests/test_worked_example.py` — the **drift-catcher**: locks the doxorubicin/A549 worked
  example (S′≈6.70) so a convention or arithmetic change can't silently diverge from the paper.

## The one open item — E_max convention (concerns.csv C1)
S′ is computed on the **percent** E_max scale (0–100). `emax_as_percent` is an input-unit
adapter, not a scale switch — fraction input is rescaled to percent internally, so both paths
give the same percent-scale S′. This scale sets the ±2/±4 thresholds. **OPEN:** confirm the
percent scale matches the *reference SPrime implementation's* output before tagging a release.
This is external reconciliation, not a code change.

## Build / test
    pip install -e .
    pytest                    # runs the drift-catcher

Worked-example reference values (from working-materials/corrected_worked_examples_S-prime.md):
S′(doxorubicin, A549) = 6.70; cohort pS′ (RB1-mut) = 8.15; S′ is unit-invariant (nM vs µM).

## Conventions
- Match surrounding style; keep the math in `core.py` and let `sprime-lung-sl` do the I/O.
- Any change to the formula, C_ref, or the percent scale MUST keep `tests/` green (or the test
  is updated deliberately, with the worked-examples doc updated in lockstep).

## License / cite
MIT (code). `CITATION.cff` lists the manuscript author team; mint a Zenodo DOI on first release.
