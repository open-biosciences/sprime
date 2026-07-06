# sprime

**S′ (S-prime) — an operational potency–efficacy index for high-throughput drug-viability screening.**

`sprime` computes a direction-preserving, variance-stabilized index that integrates potency and
efficacy from 4-parameter-logistic (4PL) dose–response fits, together with its cohort (`pS′`) and
genotype-contrast (`ΔpS′`) forms. Unlike AUC or EC₅₀, S′ encodes *polarity* — inhibition vs
disinhibition/activation — through the sign of E_max.

    S′  = asinh( (E_max / EC50) × C_ref )      # C_ref = 1 µM reference concentration
    pS′ = mean_i S′_i     over a cohort (e.g. all WT or all mutant lines)
    ΔpS′ = pS′_WT − pS′_mutant

## Status
Pre-peer-review method module accompanying Zamora et al. (S′ index; manuscript in preparation).
A peer-reviewed predecessor (log-based combined effectiveness–potency score) appears in
Zamora et al., *Cancers* 2023, 15(24):5811 (doi:10.3390/cancers15245811).

## ⚠ Open definition to confirm
S′ is computed on the **percent** `E_max` scale (0–100); `emax_as_percent` is an input-unit adapter,
not a scale switch (fraction input is rescaled to percent internally). The percent scale sets the
absolute S′ values and therefore the ±2/±4 thresholds. Open item: confirm this matches the reference
SPrime implementation's output scale before tagging a release. See `emax_as_percent` in `sprime.core`
and the reconciliation test in `tests/`.

## Install (editable)
    pip install -e .

## Quick use
    from sprime import s_prime, pooled_ps, delta_ps
    s = s_prime(emax=99.9, ec50_uM=0.245)     # percent-E_max convention

## Cite
See `CITATION.cff`. Mint a Zenodo DOI on first release.

## License
MIT (code). See `LICENSE`. Confirm the intended license with the Open Biosciences org.
