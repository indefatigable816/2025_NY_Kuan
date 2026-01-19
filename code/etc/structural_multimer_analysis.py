import os
import glob
import json
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

# Config
# Support both possible locations for the flattened multimer files
possible_a = Path(r"c:\Users\indef\Documents\NY\project\snakemake2\multimer_flattened")
possible_b = Path(r"c:\Users\indef\Documents\NY\project\snakemake2\results\multimer_flattened")
if possible_a.exists():
    SRC_DIR = possible_a
elif possible_b.exists():
    SRC_DIR = possible_b
else:
    SRC_DIR = possible_a

OUT_DIR = Path(r"c:\Users\indef\Documents\NY\project\snakemake2\structural_analysis_multimer")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Hypotheses mapping
HYPOTHESES = [
    {'drug':'Trastuzumab','mutant':'Δ16','mutant_patterns':['d16','d16_trastuzumab','d16_dimer'],'wt_pattern':'WT_trastuzumab'},
    {'drug':'Pertuzumab','mutant':'S310F','mutant_patterns':['s310f','s310f_pertuzumab'],'wt_pattern':'WT_pertuzumab'},
    {'drug':'Lapatinib','mutant':'L755S','mutant_patterns':['l755s','l755s_lapatinib'],'wt_pattern':'WT_lapatinib'},
    {'drug':'Lapatinib','mutant':'K753E','mutant_patterns':['k753e','k753e_lapatinib'],'wt_pattern':'WT_lapatinib'},
]

# Helpers

def extract_sample(basename: str) -> str:
    s = basename
    if s.startswith('confidence_'):
        s = s[len('confidence_'):]
    parts = s.split('_')
    if 'model' in parts:
        i = parts.index('model')
        sample = '_'.join(parts[:i])
    else:
        sample = parts[0]
    return sample

def extract_iptm(j: dict) -> float:
    # Prefer top-level 'iptm'
    if 'iptm' in j and isinstance(j['iptm'], (int,float)):
        return float(j['iptm'])
    # Try pair_chains_iptm nested dict
    pc = j.get('pair_chains_iptm')
    if isinstance(pc, dict):
        vals = []
        for a in pc.values():
            if isinstance(a, dict):
                for b in a.values():
                    if isinstance(b,(int,float)):
                        vals.append(b)
            elif isinstance(a,(int,float)):
                vals.append(a)
        if vals:
            return float(np.mean(vals))
    return np.nan

def extract_ptm(j: dict) -> float:
    # pTM stored as 'ptm' often
    if 'ptm' in j and isinstance(j['ptm'], (int,float)):
        return float(j['ptm'])
    # fallback to confidence_score or complex_plddt? prefer ptm
    return float(j.get('ptm', np.nan))

# Load and parse JSON files
rows = []
files = sorted(SRC_DIR.glob('*.json'))
for f in files:
    try:
        with open(f,'r',encoding='utf-8') as fh:
            j = json.load(fh)
    except Exception:
        continue
    basename = f.stem
    sample = extract_sample(basename)
    iptm = extract_iptm(j)
    ptm = extract_ptm(j)
    # skip if ptm missing or iptm missing
    if np.isnan(iptm) or np.isnan(ptm):
        continue
    rows.append({'file':str(f), 'basename':basename, 'sample':sample, 'iptm':iptm, 'ptm':ptm})

if len(rows)==0:
    print('No valid JSON files parsed.')
    raise SystemExit(1)

df = pd.DataFrame(rows)
# Apply quality filter: only include ptm > 0.5
df = df[df['ptm']>0.5].copy()
if df.empty:
    print('No records pass pTM>0.5 filter.')
    raise SystemExit(1)

# Annotate drug and mutation group

def assign_labels(sample: str):
    s = sample.lower()
    # drug detection
    if 'trastuzumab' in s:
        drug = 'Trastuzumab'
    elif 'pertuzumab' in s:
        drug = 'Pertuzumab'
    elif 'lapatinib' in s:
        drug = 'Lapatinib'
    else:
        drug = None
    # mutation detection
    if any(p in s for p in ['d16','d16_dimer']):
        mut = 'Δ16'
    elif 's310f' in s:
        mut = 'S310F'
    elif 'l755s' in s:
        mut = 'L755S'
    elif 'k753e' in s:
        mut = 'K753E'
    elif s.startswith('wt') or s.startswith('wt_'):
        mut = 'WT'
    else:
        mut = None
    # group
    group = 'Mutant' if mut and mut!='WT' else ('WT' if mut=='WT' else 'Unknown')
    return drug, mut, group

labels = df['sample'].apply(assign_labels)
labels_df = pd.DataFrame(labels.tolist(), columns=['drug','mutation','group'])
df = pd.concat([df.reset_index(drop=True), labels_df], axis=1)
# drop Unknowns
df = df[df['drug'].notnull()].copy()

# Aggregation per hypothesis
summary = []
for h in HYPOTHESES:
    drug = h['drug']
    mutant_label = h['mutant']
    # WT selection: sample contains wt_pattern OR mutation==WT and drug matches
    wt_rows = df[(df['drug']==drug) & ((df['mutation']=='WT') | (h['wt_pattern'].lower() in df['sample'].str.lower()))]
    # Mutant selection: any sample containing any mutant pattern
    mutant_mask = pd.Series(False, index=df.index)
    for p in h['mutant_patterns']:
        mutant_mask = mutant_mask | df['sample'].str.contains(p, case=False, na=False)
    mutant_rows = df[(df['drug']==drug) & mutant_mask]
    wt_n = len(wt_rows)
    mut_n = len(mutant_rows)
    wt_mean = wt_rows['iptm'].mean() if wt_n>0 else np.nan
    wt_sd = wt_rows['iptm'].std(ddof=0) if wt_n>0 else np.nan
    mut_mean = mutant_rows['iptm'].mean() if mut_n>0 else np.nan
    mut_sd = mutant_rows['iptm'].std(ddof=0) if mut_n>0 else np.nan
    delta = mut_mean - wt_mean if (not np.isnan(mut_mean) and not np.isnan(wt_mean)) else np.nan
    summary.append({
        'Drug':drug,
        'Mutation':mutant_label,
        'WT_mean':wt_mean,'WT_sd':wt_sd,'WT_n':wt_n,
        'Mutant_mean':mut_mean,'Mutant_sd':mut_sd,'Mutant_n':mut_n,
        'Delta_iPTM':delta
    })

summary_df = pd.DataFrame(summary)
summary_csv = OUT_DIR / 'multimer_summary_ipTM.csv'
summary_df.to_csv(summary_csv, index=False)
print(f'Summary saved: {summary_csv}')

# Produce boxplots / violin plots (one figure per hypothesis)
sns.set(style='whitegrid')
for h in HYPOTHESES:
    drug = h['drug']
    mutant_label = h['mutant']
    # Build plot dataframe with only relevant rows
    wt_mask = (df['drug']==drug) & ((df['mutation']=='WT') | (h['wt_pattern'].lower() in df['sample'].str.lower()))
    mutant_mask = (df['drug']==drug)
    for p in h['mutant_patterns']:
        mutant_mask = mutant_mask & (df['sample'].str.contains(p, case=False, na=False) | mutant_mask)
    plot_df = df[(df['drug']==drug) & ( (df['sample'].str.contains(h['wt_pattern'], case=False, na=False)) | df['sample'].str.contains('|'.join(h['mutant_patterns']), case=False, na=False) | (df['mutation'].isin([mutant_label,'WT'])) )].copy()
    if plot_df.empty:
        continue
    # Create column for plotting group label
    plot_df['plot_group'] = plot_df['mutation'].fillna('Other')
    # Replace WT label to 'WT (control)'
    plot_df.loc[plot_df['plot_group']=='WT','plot_group']='WT (control)'

    plt.figure(figsize=(8,6))
    # palette maps hue values 'WT' and 'Mutant'
    ax = sns.boxplot(data=plot_df, x='plot_group', y='iptm', hue='group', palette={'WT':'#2E86AB','Mutant':'#A23B72'})
    ax.set_title(f'iPTM for {drug}: Mutant vs WT')
    ax.set_xlabel('Group')
    ax.set_ylabel('iPTM (drug–target)')
    ax.legend(title='Group')
    plt.tight_layout()
    outfig = OUT_DIR / f'{drug}_{mutant_label}_iPTM_boxplot.png'
    plt.savefig(outfig, dpi=300)
    plt.close()
    print(f'Saved plot: {outfig}')

# Also save filtered full dataset
full_csv = OUT_DIR / 'multimer_filtered_dataset.csv'
df.to_csv(full_csv, index=False)
print(f'Filtered full dataset saved: {full_csv}')

# End
print('\nDone')
