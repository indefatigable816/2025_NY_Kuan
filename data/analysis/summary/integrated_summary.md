# Integrated AF3 & Boltz2 Analysis Summary

## Overview
This table integrates AF3 and Boltz2 iPTM predictions for Drug–Target complexes under mechanistic perturbation hypotheses.

| Drug | Mutant/Variant | WT Identifier | Expected Outcome (iPTM) | Mechanistic Rationale | Boltz2 iPTM | Boltz2 ΔiPTM | AF3 iPTM | AF3 ΔiPTM |
|------|--------|-------------|---------|-----------|---|---|---|---|
| Trastuzumab | Δ16 | WT (n=17) | Decrease | Homodimerization impairs antibody binding; reduced interface confidence expected | 0.4911 | −0.0027 | 0.346 | −0.0524 |
| Pertuzumab | S310F | WT (n=18) | Decrease | Mutation hypothesized to reduce binding stability; lower iPTM expected | 0.5237 | +0.0755 | 0.4045 | +0.0093 |
| Lapatinib | L755S | WT (n=20) | Decrease | L755S expected to disrupt kinase domain; lower interface confidence expected | 0.9613 | +0.3018 | N/A | N/A |
| Lapatinib | K753E | WT (n=20) | Decrease | K753E expected to disrupt kinase domain; lower interface confidence expected | 0.9634 | +0.3039 | N/A | N/A |

## Key Observations

### Hypothesis Support
- **Trastuzumab/Δ16**: Both models show decreased ΔiPTM (Boltz2: −0.0027; AF3: −0.0524). AF3 shows **strong support** (5.24% reduction); Boltz2 shows marginal decrease.
- **Pertuzumab/S310F**: Both models contradict expectation with positive ΔiPTM (Boltz2: +0.0755; AF3: +0.0093). Mutant shows higher interface confidence, not lower.
- **Lapatinib/L755S & K753E**: Boltz2 shows substantial positive ΔiPTM (+0.30), contradicting the hypothesis. AF3 data unavailable for these variants.

### Model Discrepancies
- Boltz2 and AF3 show opposite ΔiPTM directions for Pertuzumab/S310F (Boltz2: +0.0755 vs AF3: +0.0093; both positive but magnitude differs).
- Boltz2 predicts much larger confidence gains for Lapatinib variants compared to AF3's absence of data.
- Overall model agreement is partial; interpretation requires context-specific validation.

## Assumptions & Notes

1. **ΔiPTM Definition**: Calculated as Mutant iPTM − WT iPTM (mean values).
2. **Missing AF3 Data**: Lapatinib variants (L755S, K753E) lack AF3 predictions; marked as N/A.
3. **WT Baselines**:
   - Trastuzumab WT: 0.4938 (Boltz2), 0.3984 (AF3)
   - Pertuzumab WT: 0.4482 (Boltz2), 0.3952 (AF3)
   - Lapatinib WT: 0.6595 (Boltz2), no AF3 data
4. **Mechanistic Rationale**: Extracted from MD files; expectations derived from structural hypothesis that mutations destabilize interfaces.
5. **iPTM Metric**: Interpreted as interface confidence (0–1 scale); higher = more stable prediction. Decreases support disruption hypotheses.
6. **Statistical Context**: AF3 analysis based on n=5–25 per variant; Boltz2 based on n=15–20. Sample size differences may affect stability.

## Interpretation Rules
- **ΔiPTM < 0**: Supports hypothesis (predicted destabilization).
- **ΔiPTM > 0**: Contradicts hypothesis (unexpected stabilization).
- **|ΔiPTM| < 0.01**: Marginal effect (biological significance unclear).
- **|ΔiPTM| > 0.10**: Substantial effect (likely biologically relevant).
