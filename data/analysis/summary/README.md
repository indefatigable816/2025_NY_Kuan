# AF3 & Boltz2 Integration Analysis — README

## Quick Start

### Prerequisites
```bash
pip install pandas seaborn matplotlib numpy
```

### Run Analysis
```bash
python analyze_and_plot.py
```

**Output**: Three publication-ready figures + processed data CSV saved to `results/` directory.

---

## Files Generated

### Summary Tables
- **`integrated_summary.csv`** — Structured data (Drug, Variant, iPTM values, ΔiPTM, mechanistic rationale)
- **`integrated_summary.md`** — Human-readable markdown table with interpretations and key observations

### Visualization Script
- **`analyze_and_plot.py`** — Standalone Python script (no Jupyter required)
  - Reads `integrated_summary.csv`
  - Generates 3 publication-ready figures
  - Prints summary statistics and hypothesis support assessment

### Documentation
- **`ASSUMPTIONS_AND_NOTES.md`** — Comprehensive technical notes
  - Data source completeness
  - Metric definitions & assumptions
  - Discrepancies and resolutions
  - Statistical considerations
  - Mechanistic interpretation rules

---

## Output Figures

**All saved to `results/` at 300 DPI (publication-ready)**

### 1. `iptm_comparison_bars.png`
Grouped bar plot comparing ΔiPTM across AF3 and Boltz2 models.
- **Use**: Publication main figure; direct model comparison
- **Shows**: ΔiPTM per variant, grouped by model

### 2. `iptm_comparison_scatter.png`
Scatter plot (AF3 vs Boltz2) with diagonal agreement line.
- **Use**: Model concordance assessment; identifies systematic biases
- **Shows**: Correlation between models; outliers

### 3. `iptm_comparison_heatmap.png`
Color-coded matrix of ΔiPTM values.
- **Use**: Rapid visual summary; effect magnitude at a glance
- **Shows**: Direction (red=increase, blue=decrease) and magnitude

---

## Data Interpretation

### Hypothesis Support Rules
| ΔiPTM | Meaning | Hypothesis |
|-------|---------|-----------|
| **ΔiPTM < 0** | Interface confidence decreases | ✓ **SUPPORTS** (destabilization) |
| **ΔiPTM > 0** | Interface confidence increases | ✗ **CONTRADICTS** (stabilization) |
| **\|ΔiPTM\| < 0.01** | Marginal change | Biologically unclear |
| **\|ΔiPTM\| ≥ 0.10** | Substantial change | Likely biologically relevant |

### Key Findings

#### Trastuzumab / Δ16
- **AF3**: ΔiPTM = −0.0524 (−5.24%) → **Strong support** ✓
- **Boltz2**: ΔiPTM = −0.0027 (−0.27%) → **Weak support** ✓
- **Interpretation**: Homodimerization hypothesis supported; AF3 shows stronger effect

#### Pertuzumab / S310F
- **AF3**: ΔiPTM = +0.0093 (+0.93%) → **Contradicts**
- **Boltz2**: ΔiPTM = +0.0755 (+7.55%) → **Contradicts**
- **Interpretation**: Mutation increases interface confidence (opposite to hypothesis)

#### Lapatinib / L755S & K753E
- **AF3**: N/A (not available)
- **Boltz2**: ΔiPTM ≈ +0.30 (+30%) → **Strong contradiction**
- **Interpretation**: Mutations unexpectedly increase interface confidence; contradicts destabilization hypothesis

---

## Technical Details

### Data Flow
```
AF3_summary.csv           ┐
Boltz2_summary.csv        ├─> integrated_summary.csv ──> analyze_and_plot.py ──> results/
AF3_summary.md            │                                  ├─> iptm_comparison_bars.png
Boltz2_summary.md         ┘                                  ├─> iptm_comparison_scatter.png
                                                             ├─> iptm_comparison_heatmap.png
                                                             └─> delta_comparison_long.csv
```

### Script Structure
1. **Load Data**: Read `integrated_summary.csv`
2. **Reshape**: Convert to long-form for visualization (Model as categorical)
3. **Validate**: Check for missing values; handle N/A entries
4. **Plot**: Generate 3 figures with seaborn + matplotlib
5. **Summary**: Print descriptive statistics and hypothesis assessment
6. **Export**: Save figures (PNG, 300 DPI) and processed data

### Dependencies
- **pandas**: Data manipulation & CSV I/O
- **seaborn**: High-level statistical visualization
- **matplotlib**: Underlying plotting library
- **numpy**: Numerical operations

---

## Assumptions & Caveats

### Key Assumptions
1. **ΔiPTM = Mutant Mean − WT Mean** (calculated within each model separately)
2. **iPTM interpretation**: Higher = more stable interface prediction (not direct binding affinity)
3. **AF3 & Boltz2 are independent models**: Different baselines, confidence metrics, training data
4. **Hypothesis validation**: Purely computational; requires experimental confirmation

### Known Discrepancies
- **WT iPTM baselines differ** between models (Boltz2 ~5–10% higher)
- **Pertuzumab S310F**: Magnitude differs 8× between models; both contradict hypothesis
- **Lapatinib variants**: AF3 data absent; Boltz2 shows large positive ΔiPTM (paradoxical)

**See `ASSUMPTIONS_AND_NOTES.md` for detailed discussion.**

---

## Customization

### Modify Plots
Edit `analyze_and_plot.py`:
- **Colors**: Change `PALETTE` dict (line ~24)
- **Figure size**: Adjust `FIGURE_SIZE` tuple (line ~23)
- **DPI**: Change `FIGURE_DPI` (line ~22)
- **Font size**: Modify `FONT_SIZE` (line ~25)

### Add Variants
1. Add row to `integrated_summary.csv`
2. Re-run script; figures regenerate automatically

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'seaborn'` | Run `pip install seaborn` |
| `FileNotFoundError: integrated_summary.csv` | Ensure CSV is in same directory as script |
| Figures look low-quality | Check `FIGURE_DPI` (set to 300 for publication) |
| Missing AF3 bars | Correct; Lapatinib variants have AF3 = N/A |

---

## Citation

**Data**: AF3 & Boltz2 structure predictions  
**Analysis**: Integrated ΔiPTM comparison  
**Figures**: Publication-ready (seaborn, 300 DPI)  
**Generated**: 2026-01-19

---

**For detailed technical information, see `ASSUMPTIONS_AND_NOTES.md`**
