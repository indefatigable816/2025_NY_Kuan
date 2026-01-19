#!/usr/bin/env python3
"""
Integrated AF3 & Boltz2 Analysis and Visualization
===================================================
Generates publication-ready comparisons of iPTM predictions across models.

Author: Data Analysis Pipeline
Date: 2026-01-19
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Input files
INPUT_DIR = Path(".")
AF3_CSV = INPUT_DIR / "AF3_summary.csv"
BOLTZ2_CSV = INPUT_DIR / "boltz2_summary.csv"
INTEGRATED_CSV = INPUT_DIR / "integrated_summary.csv"

# Output directory
OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

# Plotting parameters
FIGURE_DPI = 300
FIGURE_SIZE = (12, 7)
FONT_SIZE = 11
PALETTE = {"AF3": "#1f77b4", "Boltz2": "#ff7f0e"}

# ============================================================================
# DATA LOADING & PREPARATION
# ============================================================================

def load_data():
    """Load and merge AF3 and Boltz2 data."""
    print("[INFO] Loading integrated summary...")
    integrated = pd.read_csv(INTEGRATED_CSV)
    return integrated


def prepare_delta_comparison(df):
    """
    Reshape data for ΔiPTM comparison visualization.
    Creates long-form data with model as categorical variable.
    """
    data_long = []
    
    for _, row in df.iterrows():
        drug = row["Drug"]
        variant = row["Mutant/Variant"]
        label = f"{drug} / {variant}"
        
        # Boltz2 entry
        if pd.notna(row["Boltz2 ΔiPTM"]):
            # Parse the sign prefix if present
            boltz2_delta = float(str(row["Boltz2 ΔiPTM"]).replace("−", "-"))
            data_long.append({
                "Drug": drug,
                "Variant": variant,
                "Label": label,
                "Model": "Boltz2",
                "ΔiPTM": boltz2_delta,
            })
        
        # AF3 entry
        if pd.notna(row["AF3 ΔiPTM"]) and row["AF3 ΔiPTM"] != "N/A":
            af3_delta = float(str(row["AF3 ΔiPTM"]).replace("−", "-"))
            data_long.append({
                "Drug": drug,
                "Variant": variant,
                "Label": label,
                "Model": "AF3",
                "ΔiPTM": af3_delta,
            })
    
    return pd.DataFrame(data_long)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_delta_comparison(df_long):
    """
    Generate grouped bar plot comparing ΔiPTM across models.
    
    Shows:
    - X-axis: Drug / Variant combinations
    - Y-axis: ΔiPTM (Mutant iPTM - WT iPTM)
    - Hue: Model (AF3 vs Boltz2)
    - Horizontal line at y=0 for reference
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
    
    # Generate plot
    sns.barplot(
        data=df_long,
        x="Label",
        y="ΔiPTM",
        hue="Model",
        palette=PALETTE,
        ax=ax,
        width=0.7,
    )
    
    # Formatting
    ax.set_xlabel("Drug / Variant", fontsize=FONT_SIZE, fontweight="bold")
    ax.set_ylabel("ΔiPTM (Mutant − WT)", fontsize=FONT_SIZE, fontweight="bold")
    ax.set_title(
        "AF3 vs Boltz2 Interface Confidence Predictions (ΔiPTM)",
        fontsize=FONT_SIZE + 2,
        fontweight="bold",
        pad=20,
    )
    
    # Reference line at zero
    ax.axhline(y=0, color="black", linestyle="--", linewidth=1.5, alpha=0.6, label="No Change")
    
    # Rotate x-axis labels for readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=FONT_SIZE)
    ax.tick_params(axis="y", labelsize=FONT_SIZE)
    
    # Legend
    ax.legend(
        title="Model",
        fontsize=FONT_SIZE - 1,
        title_fontsize=FONT_SIZE,
        loc="best",
        frameon=True,
    )
    
    # Grid for readability
    ax.grid(axis="y", alpha=0.3, linestyle=":", linewidth=0.8)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    # Save
    output_path = OUTPUT_DIR / "iptm_comparison_bars.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    print(f"[SAVED] {output_path}")
    plt.close()


def plot_scatter_comparison(df_long):
    """
    Generate scatter plot with AF3 vs Boltz2 ΔiPTM values.
    
    Allows direct model comparison with optional diagonal reference.
    """
    # Pivot to get AF3 and Boltz2 side-by-side
    pivot_data = df_long.pivot_table(
        index=["Drug", "Variant"],
        columns="Model",
        values="ΔiPTM"
    ).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 8), dpi=FIGURE_DPI)
    
    # Color by drug
    drugs = pivot_data["Drug"].unique()
    colors = sns.color_palette("husl", len(drugs))
    drug_colors = {drug: colors[i] for i, drug in enumerate(drugs)}
    
    for drug in drugs:
        mask = pivot_data["Drug"] == drug
        subset = pivot_data[mask]
        
        # Only plot if both models have data
        valid = subset.dropna(subset=["AF3", "Boltz2"])
        
        if len(valid) > 0:
            ax.scatter(
                valid["AF3"],
                valid["Boltz2"],
                s=150,
                alpha=0.7,
                label=drug,
                color=drug_colors[drug],
                edgecolors="black",
                linewidth=1,
            )
            
            # Add labels for each point
            for _, point in valid.iterrows():
                ax.annotate(
                    point["Variant"],
                    (point["AF3"], point["Boltz2"]),
                    fontsize=9,
                    alpha=0.8,
                    xytext=(5, 5),
                    textcoords="offset points",
                )
    
    # Diagonal reference (perfect agreement)
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),
        np.max([ax.get_xlim(), ax.get_ylim()]),
    ]
    ax.plot(lims, lims, "k--", alpha=0.5, linewidth=1.5, label="Perfect Agreement")
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    
    # Formatting
    ax.set_xlabel("AF3 ΔiPTM", fontsize=FONT_SIZE, fontweight="bold")
    ax.set_ylabel("Boltz2 ΔiPTM", fontsize=FONT_SIZE, fontweight="bold")
    ax.set_title(
        "Model Concordance: AF3 vs Boltz2 ΔiPTM Predictions",
        fontsize=FONT_SIZE + 2,
        fontweight="bold",
        pad=20,
    )
    
    # Grid and legend
    ax.grid(True, alpha=0.3, linestyle=":")
    ax.legend(fontsize=FONT_SIZE - 1, loc="best", frameon=True)
    
    # Add zero lines for reference
    ax.axhline(y=0, color="gray", linestyle=":", alpha=0.5)
    ax.axvline(x=0, color="gray", linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    
    # Save
    output_path = OUTPUT_DIR / "iptm_comparison_scatter.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    print(f"[SAVED] {output_path}")
    plt.close()


def plot_model_agreement(df_long):
    """
    Generate heatmap showing model agreement and effect magnitude.
    """
    # Create matrix: rows = Drug/Variant, columns = Model
    pivot = df_long.pivot_table(
        index=["Drug", "Variant"],
        columns="Model",
        values="ΔiPTM"
    )
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=FIGURE_DPI)
    
    # Heatmap
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".4f",
        cmap="RdBu_r",
        center=0,
        cbar_kws={"label": "ΔiPTM"},
        ax=ax,
        linewidths=0.5,
        linecolor="gray",
    )
    
    # Formatting
    ax.set_title(
        "ΔiPTM Heatmap: Model Predictions (Red = Increase, Blue = Decrease)",
        fontsize=FONT_SIZE + 1,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Model", fontsize=FONT_SIZE, fontweight="bold")
    ax.set_ylabel("Drug / Variant", fontsize=FONT_SIZE, fontweight="bold")
    
    plt.tight_layout()
    
    # Save
    output_path = OUTPUT_DIR / "iptm_comparison_heatmap.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    print(f"[SAVED] {output_path}")
    plt.close()


# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

def print_summary_stats(df, df_long):
    """Print descriptive statistics and hypothesis support summary."""
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    print("\n[ΔiPTM by Model]")
    summary = df_long.groupby("Model")["ΔiPTM"].describe()
    print(summary)
    
    print("\n[Hypothesis Support]")
    print("Note: ΔiPTM < 0 = supports hypothesis (destabilization)")
    print("      ΔiPTM > 0 = contradicts hypothesis (stabilization)\n")
    
    for _, row in df.iterrows():
        drug = row["Drug"]
        variant = row["Mutant/Variant"]
        expected = row["Expected Outcome (iPTM)"]
        boltz2_delta = row["Boltz2 ΔiPTM"]
        af3_delta = row["AF3 ΔiPTM"]
        
        print(f"{drug} / {variant}:")
        print(f"  Expected: {expected}")
        
        if pd.notna(boltz2_delta):
            boltz2_val = float(str(boltz2_delta).replace("−", "-"))
            support = "✓ Support" if boltz2_val < 0 else "✗ Contradict"
            print(f"  Boltz2 ΔiPTM = {boltz2_val:+.4f} {support}")
        
        if pd.notna(af3_delta) and af3_delta != "N/A":
            af3_val = float(str(af3_delta).replace("−", "-"))
            support = "✓ Support" if af3_val < 0 else "✗ Contradict"
            print(f"  AF3 ΔiPTM    = {af3_val:+.4f} {support}")
        else:
            print(f"  AF3 ΔiPTM    = N/A")
        print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main analysis pipeline."""
    print("[START] AF3 & Boltz2 Integration Analysis")
    print(f"[INFO] Output directory: {OUTPUT_DIR.absolute()}\n")
    
    # Load data
    df = load_data()
    df_long = prepare_delta_comparison(df)
    
    # Generate visualizations
    print("\n[PLOTTING] Generating figures...")
    plot_delta_comparison(df_long)
    plot_scatter_comparison(df_long)
    plot_model_agreement(df_long)
    
    # Print summary
    print_summary_stats(df, df_long)
    
    # Save processed data
    output_csv = OUTPUT_DIR / "delta_comparison_long.csv"
    df_long.to_csv(output_csv, index=False)
    print(f"\n[SAVED] {output_csv}")
    
    print("\n[COMPLETE] Analysis finished successfully.")


if __name__ == "__main__":
    main()
