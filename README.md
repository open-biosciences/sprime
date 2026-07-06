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
`E_max` convention (fraction 0–1 vs percent 0–100) is **not yet locked** — it sets the absolute S′
scale and therefore any thresholds. See `emax_as_percent` in `sprime.core` and the reconciliation
test in `tests/`. Resolve against the reference implementation before tagging a release.

## Install (editable)
    pip install -e .

## Quick use
    from sprime import s_prime, pooled_ps, delta_ps
    s = s_prime(emax=99.9, ec50_uM=0.245)     # percent-E_max convention

## Cite
See `CITATION.cff`. Mint a Zenodo DOI on first release.

## License
MIT (code). See `LICENSE`. Confirm the intended license with the Open Biosciences org.
