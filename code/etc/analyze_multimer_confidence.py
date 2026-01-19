#!/usr/bin/env python3
"""
AlphaFold3 Multimer Confidence Analysis
Analyzes iPTM metrics across HER2 variants and antibody conditions.

Focus: HER2 Δ16/S310F mutants vs WT control with Trastuzumab/Pertuzumab
Primary metric: Interface confidence (iPTM)
Validity filter: pTM > 0.5
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_DIR = Path(r"c:\Users\indef\Documents\NY\project\data\results\AF3\multimer")
OUTPUT_DIR = Path(r"c:\Users\indef\Documents\NY\project\data\results\AF3")
PTM_THRESHOLD = 0.5

# =============================================================================
# SECTION 1: FILE DISCOVERY AND VALIDATION
# =============================================================================
print("=" * 100)
print("SECTION 1: FILE DISCOVERY AND VALIDATION")
print("=" * 100)

# Recursively find all fold*summary_confidences*.json files
json_files = sorted(list(BASE_DIR.rglob("fold*summary_confidences*.json")))

print(f"\nTotal JSON files found: {len(json_files)}")
print(f"\nExpected data categories:")
print("  • HER2 Δ16 + Trastuzumab (Experimental)")
print("  • HER2 WT + Trastuzumab (Control)")
print("  • HER2 S310F + Pertuzumab (Experimental)")
print("  • HER2 WT + Pertuzumab (Control)")

print(f"\nSample file paths:")
for f in json_files[:5]:
    print(f"  {f.relative_to(BASE_DIR.parent)}")

# =============================================================================
# SECTION 2: JSON PARSING AND DATA EXTRACTION
# =============================================================================
print("\n" + "=" * 100)
print("SECTION 2: JSON PARSING AND DATA EXTRACTION")
print("=" * 100)

def parse_metadata_from_path(file_path):
    """Extract Drug, Variant, and Group from file path."""
    parts = file_path.parts
    parent_dir = parts[-2]  # e.g., 'd16_trastuzumab_1'
    
    # Extract drug and variant
    if 'trastuzumab' in parent_dir.lower():
        drug = 'Trastuzumab'
    elif 'pertuzumab' in parent_dir.lower():
        drug = 'Pertuzumab'
    else:
        drug = 'Unknown'
    
    # Extract variant and group
    if 'd16_trastuzumab' in parent_dir.lower():
        variant = 'Δ16'
        group = 'Experimental'
    elif 'wt_trastuzumab' in parent_dir.lower():
        variant = 'WT'
        group = 'Control'
    elif 's310f_pertuzumab' in parent_dir.lower():
        variant = 'S310F'
        group = 'Experimental'
    elif 'wt_pertuzumab' in parent_dir.lower():
        variant = 'WT'
        group = 'Control'
    else:
        variant = 'Unknown'
        group = 'Unknown'
    
    return drug, variant, group

def extract_confidence_metrics(json_path):
    """Parse JSON and extract iPTM, pTM, and model identifier."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Extract metrics - handle various possible structures
        iptm = data.get('iptm', None)
        ptm = data.get('pTM', data.get('ptm', None))
        
        # If metrics are nested, try common paths
        if iptm is None and 'metrics' in data:
            iptm = data['metrics'].get('iptm', None)
        if ptm is None and 'metrics' in data:
            ptm = data['metrics'].get('pTM', data['metrics'].get('ptm', None))
        
        # Extract model identifier from filename
        filename = json_path.stem
        model_id = filename.split('_')[-1] if '_' in filename else 'unknown'
        
        return {
            'iptm': iptm,
            'ptm': ptm,
            'model_id': model_id,
            'file_path': str(json_path)
        }
    except Exception as e:
        print(f"  ⚠ Error parsing {json_path.name}: {e}")
        return None

# Parse all JSON files
raw_data = []
parse_errors = 0

print("\nParsing JSON files...")
for json_path in json_files:
    metrics = extract_confidence_metrics(json_path)
    if metrics:
        drug, variant, group = parse_metadata_from_path(json_path)
        metrics['drug'] = drug
        metrics['variant'] = variant
        metrics['group'] = group
        raw_data.append(metrics)
    else:
        parse_errors += 1

print(f"✓ Successfully parsed: {len(raw_data)} files")
print(f"✗ Parse errors: {parse_errors}")

# Create DataFrame
df_raw = pd.DataFrame(raw_data)
print(f"\nRaw data shape: {df_raw.shape}")
print(f"\nData summary:")
print(f"  iPTM - Min: {df_raw['iptm'].min():.4f}, Max: {df_raw['iptm'].max():.4f}, Mean: {df_raw['iptm'].mean():.4f}")
print(f"  pTM  - Min: {df_raw['ptm'].min():.4f}, Max: {df_raw['ptm'].max():.4f}, Mean: {df_raw['ptm'].mean():.4f}")
print(f"  Missing iPTM: {df_raw['iptm'].isna().sum()}")
print(f"  Missing pTM: {df_raw['ptm'].isna().sum()}")

# =============================================================================
# SECTION 3: DATA FILTERING AND QUALITY CONTROL
# =============================================================================
print("\n" + "=" * 100)
print("SECTION 3: DATA FILTERING AND QUALITY CONTROL")
print("=" * 100)

# Filter: pTM > 0.5 (structural validity)
df_filtered = df_raw[(df_raw['ptm'] > PTM_THRESHOLD)].copy()

print(f"\nStructural Validity Filter (pTM > {PTM_THRESHOLD}):")
print(f"  Records before filter: {len(df_raw)}")
print(f"  Records after filter:  {len(df_filtered)}")
print(f"  Records excluded:      {len(df_raw) - len(df_filtered)}")
print(f"  Retention rate:        {100 * len(df_filtered) / len(df_raw):.1f}%")

# Breakdown by drug and variant
print(f"\nFiltered records by Drug and Variant:")
breakdown = df_filtered.groupby(['drug', 'variant']).size()
for (drug, variant), count in breakdown.items():
    print(f"  {drug:15} + {variant:6}: {count:4} valid models (pTM > {PTM_THRESHOLD})")

# =============================================================================
# SECTION 4: AGGREGATION AND SUMMARY STATISTICS
# =============================================================================
print("\n" + "=" * 100)
print("SECTION 4: AGGREGATION AND SUMMARY STATISTICS")
print("=" * 100)

# Generate summary statistics by Drug, Variant, and Group
summary_stats = []

for (drug, variant), group_data in df_filtered.groupby(['drug', 'variant']):
    group = group_data['group'].iloc[0]  # All records in group have same label
    
    iptm_values = group_data['iptm'].dropna()
    n_models = len(iptm_values)
    mean_iptm = iptm_values.mean()
    median_iptm = iptm_values.median()
    std_iptm = iptm_values.std()
    
    summary_stats.append({
        'Drug': drug,
        'Variant': variant,
        'Group': group,
        'Mean iPTM': mean_iptm,
        'Median iPTM': median_iptm,
        'Std Dev': std_iptm,
        'N': n_models
    })

df_summary = pd.DataFrame(summary_stats).sort_values(['Drug', 'Variant'])

# Calculate ΔiPTM vs WT for each drug
delta_iptm_results = []
for drug in df_summary['Drug'].unique():
    drug_data = df_summary[df_summary['Drug'] == drug]
    wt_mean = drug_data[drug_data['Variant'] == 'WT']['Mean iPTM'].values
    
    if len(wt_mean) > 0:
        wt_mean = wt_mean[0]
        for _, row in drug_data.iterrows():
            if row['Variant'] != 'WT':
                delta = row['Mean iPTM'] - wt_mean
                delta_iptm_results.append({
                    'Drug': drug,
                    'Variant': row['Variant'],
                    'ΔiPTM vs WT': delta
                })

df_delta = pd.DataFrame(delta_iptm_results)

# Merge delta values into summary
df_summary = df_summary.merge(
    df_delta[['Drug', 'Variant', 'ΔiPTM vs WT']],
    on=['Drug', 'Variant'],
    how='left'
)

# Reorder columns
df_summary = df_summary[['Drug', 'Variant', 'Group', 'Mean iPTM', 'Median iPTM', 'N', 'ΔiPTM vs WT', 'Std Dev']]

# Display summary table
print("\n" + "=" * 120)
print("SUMMARY TABLE: AF3 iPTM Metrics by Drug, Variant, and Group (pTM > 0.5)")
print("=" * 120)
print(df_summary.to_string(index=False))
print("=" * 120)

# Save summary table to CSV
summary_csv_path = OUTPUT_DIR / "AF3_Summary_Statistics.csv"
df_summary.to_csv(summary_csv_path, index=False)
print(f"\n✓ Summary table saved: {summary_csv_path}")

# =============================================================================
# SECTION 5: HYPOTHESIS-DRIVEN COMPARATIVE ANALYSIS
# =============================================================================
print("\n" + "=" * 100)
print("SECTION 5: HYPOTHESIS-DRIVEN COMPARATIVE ANALYSIS")
print("=" * 100)

# Hypothesis 1: Trastuzumab
print("\n" + "-" * 100)
print("HYPOTHESIS 1: Trastuzumab Binding - Δ16 Homodimerization Effect")
print("-" * 100)
print("Objective: Assess if HER2 Δ16 + Trastuzumab shows LOWER iPTM than WT control")
print("Mechanistic Rationale:")
print("  Δ16 enforces covalent homodimers, distorting ECD geometry")
print("  Reduced Trastuzumab accessibility and stable engagement")
print("  Lower AF3 iPTM expected in Δ16 vs WT")

tras_data = df_filtered[df_filtered['drug'] == 'Trastuzumab'].copy()
tras_wt = tras_data[tras_data['variant'] == 'WT']['iptm'].dropna()
tras_d16 = tras_data[tras_data['variant'] == 'Δ16']['iptm'].dropna()

print(f"\nStatistics:")
print(f"  HER2 WT + Trastuzumab:   n={len(tras_wt):3d}, mean iPTM={tras_wt.mean():.4f}, median={tras_wt.median():.4f}, std={tras_wt.std():.4f}")
print(f"  HER2 Δ16 + Trastuzumab:  n={len(tras_d16):3d}, mean iPTM={tras_d16.mean():.4f}, median={tras_d16.median():.4f}, std={tras_d16.std():.4f}")

delta_tras = tras_d16.mean() - tras_wt.mean()
print(f"\n  ΔiPTM (Δ16 - WT):        {delta_tras:+.4f}")

# Statistical test
if len(tras_wt) > 0 and len(tras_d16) > 0:
    t_stat, p_value = stats.ttest_ind(tras_wt, tras_d16)
    print(f"  t-test: t={t_stat:+.4f}, p-value={p_value:.6f}")

if delta_tras < 0:
    h1_result = "LOWER in Δ16 ✓ (SUPPORTS hypothesis)"
else:
    h1_result = "HIGHER in Δ16 ✗ (CONTRADICTS hypothesis)"
print(f"\nResult: {h1_result}")

# Hypothesis 2: Pertuzumab
print("\n" + "-" * 100)
print("HYPOTHESIS 2: Pertuzumab Binding - S310F ECD II Disruption")
print("-" * 100)
print("Objective: Assess if HER2 S310F + Pertuzumab shows LOWER iPTM than WT control")
print("Mechanistic Rationale:")
print("  S310F disrupts the ECD II dimer interface critical for HER2 dimerization")
print("  Impairs Pertuzumab-mediated binding and inhibition")
print("  Lower AF3 iPTM expected in S310F vs WT")

pertz_data = df_filtered[df_filtered['drug'] == 'Pertuzumab'].copy()
pertz_wt = pertz_data[pertz_data['variant'] == 'WT']['iptm'].dropna()
pertz_s310f = pertz_data[pertz_data['variant'] == 'S310F']['iptm'].dropna()

print(f"\nStatistics:")
print(f"  HER2 WT + Pertuzumab:     n={len(pertz_wt):3d}, mean iPTM={pertz_wt.mean():.4f}, median={pertz_wt.median():.4f}, std={pertz_wt.std():.4f}")
print(f"  HER2 S310F + Pertuzumab:  n={len(pertz_s310f):3d}, mean iPTM={pertz_s310f.mean():.4f}, median={pertz_s310f.median():.4f}, std={pertz_s310f.std():.4f}")

delta_pertz = pertz_s310f.mean() - pertz_wt.mean()
print(f"\n  ΔiPTM (S310F - WT):       {delta_pertz:+.4f}")

# Statistical test
if len(pertz_wt) > 0 and len(pertz_s310f) > 0:
    t_stat2, p_value2 = stats.ttest_ind(pertz_wt, pertz_s310f)
    print(f"  t-test: t={t_stat2:+.4f}, p-value={p_value2:.6f}")

if delta_pertz < 0:
    h2_result = "LOWER in S310F ✓ (SUPPORTS hypothesis)"
else:
    h2_result = "HIGHER in S310F ✗ (CONTRADICTS hypothesis)"
print(f"\nResult: {h2_result}")

# =============================================================================
# SECTION 6: PUBLICATION-READY VISUALIZATION
# =============================================================================
print("\n" + "=" * 100)
print("SECTION 6: PUBLICATION-READY VISUALIZATION")
print("=" * 100)

# Set seaborn style
sns.set_style("whitegrid")
sns.set_palette("Set2")

# Create figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Figure 1: Trastuzumab (H1)
tras_plot_data = tras_data[['variant', 'iptm']].dropna()
sns.boxplot(
    data=tras_plot_data, 
    x='variant', 
    y='iptm', 
    ax=axes[0], 
    palette=['#2ecc71', '#e74c3c'],
    width=0.6
)
sns.stripplot(
    data=tras_plot_data, 
    x='variant', 
    y='iptm', 
    ax=axes[0], 
    color='black', 
    alpha=0.4, 
    size=5,
    jitter=True
)
axes[0].set_xlabel('HER2 Variant', fontsize=13, fontweight='bold')
axes[0].set_ylabel('iPTM (Interface Confidence)', fontsize=13, fontweight='bold')
axes[0].set_title('Hypothesis 1: Trastuzumab Binding\nHER2 WT (Control) vs Δ16 (Experimental)', 
                   fontsize=13, fontweight='bold', pad=15)
axes[0].set_xticklabels(['WT\n(Control)', 'Δ16\n(Experimental)'], fontsize=11)
axes[0].grid(axis='y', alpha=0.3)
axes[0].set_ylim(axes[0].get_ylim()[0] - 0.15, axes[0].get_ylim()[1])

# Add sample sizes and delta
for i, variant in enumerate(['WT', 'Δ16']):
    n = len(tras_data[tras_data['variant'] == variant]['iptm'].dropna())
    y_pos = axes[0].get_ylim()[0] - 0.08
    axes[0].text(i, y_pos, f'n={n}', ha='center', fontsize=10, fontweight='bold')

# Add delta annotation
axes[0].text(0.5, 0.95, f'ΔiPTM = {delta_tras:+.4f}', 
             transform=axes[0].transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=11, fontweight='bold')

# Figure 2: Pertuzumab (H2)
pertz_plot_data = pertz_data[['variant', 'iptm']].dropna()
sns.boxplot(
    data=pertz_plot_data, 
    x='variant', 
    y='iptm', 
    ax=axes[1], 
    palette=['#2ecc71', '#e67e22'],
    width=0.6
)
sns.stripplot(
    data=pertz_plot_data, 
    x='variant', 
    y='iptm', 
    ax=axes[1], 
    color='black', 
    alpha=0.4, 
    size=5,
    jitter=True
)
axes[1].set_xlabel('HER2 Variant', fontsize=13, fontweight='bold')
axes[1].set_ylabel('iPTM (Interface Confidence)', fontsize=13, fontweight='bold')
axes[1].set_title('Hypothesis 2: Pertuzumab Binding\nHER2 WT (Control) vs S310F (Experimental)', 
                  fontsize=13, fontweight='bold', pad=15)
axes[1].set_xticklabels(['WT\n(Control)', 'S310F\n(Experimental)'], fontsize=11)
axes[1].grid(axis='y', alpha=0.3)
axes[1].set_ylim(axes[1].get_ylim()[0] - 0.15, axes[1].get_ylim()[1])

# Add sample sizes and delta
for i, variant in enumerate(['WT', 'S310F']):
    n = len(pertz_data[pertz_data['variant'] == variant]['iptm'].dropna())
    y_pos = axes[1].get_ylim()[0] - 0.08
    axes[1].text(i, y_pos, f'n={n}', ha='center', fontsize=10, fontweight='bold')

# Add delta annotation
axes[1].text(0.5, 0.95, f'ΔiPTM = {delta_pertz:+.4f}', 
             transform=axes[1].transAxes, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=11, fontweight='bold')

plt.tight_layout()

# Save figure
fig_path = OUTPUT_DIR / "AF3_iPTM_Hypothesis_Comparison.png"
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Figure saved: {fig_path}")

# Close figure
plt.close()

# =============================================================================
# SECTION 7: MECHANISTIC INTERPRETATION
# =============================================================================
print("\n" + "=" * 100)
print("SECTION 7: MECHANISTIC INTERPRETATION")
print("=" * 100)

print("\n" + "-" * 100)
print("[H1] TRASTUZUMAB BINDING - Δ16 Homodimerization Effect")
print("-" * 100)

if delta_tras < -0.05:
    h1_support = "STRONG SUPPORT ✓✓"
    h1_direction = "Substantially lower iPTM in Δ16 (as predicted)"
elif delta_tras < 0:
    h1_support = "WEAK SUPPORT ✓"
    h1_direction = "Lower iPTM in Δ16, but marginal effect"
else:
    h1_support = "NO SUPPORT / CONTRADICTS ✗✗"
    h1_direction = f"Higher iPTM in Δ16 (opposite to prediction, Δ={delta_tras:+.4f})"

print(f"Observation: ΔiPTM (Δ16 - WT) = {delta_tras:+.4f}")
print(f"Direction: {h1_direction}")
print(f"Hypothesis Support: {h1_support}")
print(f"\nMechanistic Rationale:")
print(f"  • Δ16 mutation induces covalent homodimerization of HER2 ECD")
print(f"  • Homodimer formation constrains ECD geometry")
print(f"  • Reduced accessibility to Trastuzumab epitopes")
print(f"  • Lower iPTM confidence reflects compromised antibody-target engagement")
if delta_tras < 0:
    print(f"  ✓ AF3 iPTM trends ARE CONSISTENT with mechanistic hypothesis")
else:
    print(f"  ✗ AF3 iPTM trends ARE INCONSISTENT with mechanistic hypothesis")

print("\n" + "-" * 100)
print("[H2] PERTUZUMAB BINDING - S310F ECD II Disruption")
print("-" * 100)

if delta_pertz < -0.05:
    h2_support = "STRONG SUPPORT ✓✓"
    h2_direction = "Substantially lower iPTM in S310F (as predicted)"
elif delta_pertz < 0:
    h2_support = "WEAK SUPPORT ✓"
    h2_direction = "Lower iPTM in S310F, but marginal effect"
else:
    h2_support = "NO SUPPORT / CONTRADICTS ✗✗"
    h2_direction = f"Higher iPTM in S310F (opposite to prediction, Δ={delta_pertz:+.4f})"

print(f"Observation: ΔiPTM (S310F - WT) = {delta_pertz:+.4f}")
print(f"Direction: {h2_direction}")
print(f"Hypothesis Support: {h2_support}")
print(f"\nMechanistic Rationale:")
print(f"  • S310F substitution disrupts the ECD II dimer interface")
print(f"  • Impairs critical dimerization interactions")
print(f"  • Reduces Pertuzumab-mediated allosteric inhibition")
print(f"  • Lower iPTM confidence reflects compromised antibody-target engagement")
if delta_pertz < 0:
    print(f"  ✓ AF3 iPTM trends ARE CONSISTENT with mechanistic hypothesis")
else:
    print(f"  ✗ AF3 iPTM trends ARE INCONSISTENT with mechanistic hypothesis")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 100)
print("FINAL SUMMARY & CONCLUSIONS")
print("=" * 100)

print(f"\nH1 (Trastuzumab): {h1_support:40} | {h1_direction}")
print(f"H2 (Pertuzumab):  {h2_support:40} | {h2_direction}")

overall_support = (delta_tras < 0 and delta_pertz < 0)
overall_msg = "SUPPORT" if overall_support else "DO NOT FULLY SUPPORT"

print(f"\n{'═' * 100}")
print(f"AF3 iPTM trends (pTM > {PTM_THRESHOLD}) {overall_msg} the proposed mechanisms")
print(f"of reduced antibody binding in HER2 mutants.")
print(f"{'═' * 100}")

print(f"\nConclusions tied strictly to iPTM and pTM-filtered confidence metrics:")
print(f"  • Trastuzumab hypothesis: {'CONSISTENT' if delta_tras < 0 else 'INCONSISTENT'} with AF3 predictions")
print(f"  • Pertuzumab hypothesis:  {'CONSISTENT' if delta_pertz < 0 else 'INCONSISTENT'} with AF3 predictions")
print(f"  • Both hypotheses supported: {'YES ✓' if (delta_tras < 0 and delta_pertz < 0) else 'NO ✗'}")

print("\n" + "=" * 100)
print("Analysis complete. Outputs saved:")
print(f"  • Summary table: {summary_csv_path}")
print(f"  • Figure: {fig_path}")
print("=" * 100)
