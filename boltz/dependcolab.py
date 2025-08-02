#@title Install Dependencies
import os
import sys

# --- 1. Define required versions ---
# This makes it easy to update versions in the future
REQUIRED_TORCH_VERSION = "2.4.0"
REQUIRED_PL_VERSION = "2.5.0"

# A flag to determine if we need to run the installation
needs_install = False

# --- 2. Check if the correct versions are already installed ---
try:
    import torch
    import pytorch_lightning as pl

    # Check if the installed versions match our requirements.
    # We use .startswith() to ignore suffixes like "+cu118"
    torch_ok = torch.__version__.startswith(REQUIRED_TORCH_VERSION)
    pl_ok = pl.__version__.startswith(REQUIRED_PL_VERSION)

    if torch_ok and pl_ok:
        print(f"✓ Correct versions already installed.")
        print(f"  - PyTorch: {torch.__version__}")
        print(f"  - PyTorch-Lightning: {pl.__version__}")
        print("Skipping installation.")
    else:
        print("Mismatched versions detected. Reinstallation is required.")
        if not torch_ok:
            print(f"  - Found PyTorch {torch.__version__}, but require {REQUIRED_TORCH_VERSION}")
        if not pl_ok:
            print(f"  - Found PyTorch-Lightning {pl.__version__}, but require {REQUIRED_PL_VERSION}")
        needs_install = True

except ImportError:
    # This block runs if one of the libraries isn't installed at all
    print("Required libraries not found. Installation is required.")
    needs_install = True

# --- 3. Run installation and restart ONLY if needed ---
if needs_install:
    print("\nUninstalling existing PyTorch to avoid conflicts...")
    # Using sys.executable ensures we use the correct pip
    import subprocess
    subprocess.run([
        sys.executable, "-m", "pip", "uninstall",
        "torch", "torchvision", "torchaudio", "-y", "-q"
    ], check=True)

    print("Installing specified library versions...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        f"torch=={REQUIRED_TORCH_VERSION}",
        "torchvision==0.19.0",
        "--index-url", "https://download.pytorch.org/whl/cu118",
        "-q"
    ], check=True)
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        f"pytorch-lightning=={REQUIRED_PL_VERSION}",
        "boltz", "py3Dmol", "-q"
    ], check=True)
    print("Installation complete.")

    # Crucial step: Restart the runtime to load the new libraries
    print("\nIMPORTANT: Runtime is restarting to load new versions. Please wait...")
    os.kill(os.getpid(), 9)
#@title Verify Installation
import torch
import pytorch_lightning as pl
import boltz
import py3Dmol

print("✅ Dependencies loaded successfully!")
print(f"✓ PyTorch version: {torch.__version__}")
print(f"✓ PyTorch-Lightning version: {pl.__version__}")
print(f"✓ BOLTZ installed")
print(f"✓ py3Dmol installed")
print("-" * 30)
print(f"✓ GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not available'}")
#@title Import Libraries
import os
import sys
import subprocess
import json
import tempfile
import yaml
import shutil
from pathlib import Path
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import py3Dmol
from google.colab import files
from IPython.display import display, HTML
import torch

# Configure environment
os.makedirs('output', exist_ok=True)
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
gpu_info = torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only'
print(f"Device: {device} ({gpu_info})")
#@title Core BOLTZ Interface

class BOLTZPredictor:
    """Main interface for BOLTZ 2 predictions"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def run_prediction(self, input_data: dict, job_name: str,
                      use_msa: bool = True, verbose: bool = False) -> dict:
        """
        Execute BOLTZ prediction

        Args:
            input_data: YAML-compatible input dictionary
            job_name: Unique identifier for this job
            use_msa: Whether to use MSA server
            verbose: Print detailed output

        Returns:
            Dictionary containing results and file paths
        """
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(input_data, f)
            yaml_path = f.name

        # Build command
        output_path = self.output_dir / job_name
        cmd = ["boltz", "predict", yaml_path, "--out_dir", str(output_path)]

        if use_msa:
            cmd.append("--use_msa_server")

        try:
            # Execute prediction
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                return {"success": False, "error": stderr or stdout}

            # Parse results
            result_dirs = list(output_path.glob("boltz_results_*"))

            files = {"pdb": [], "cif": [], "json": []}
            for result_dir in result_dirs:
                files["pdb"].extend(list(result_dir.rglob("*.pdb")))
                files["cif"].extend(list(result_dir.rglob("*.cif")))
                files["json"].extend(list(result_dir.rglob("*.json")))

            # Load JSON results
            results = {}
            for json_file in files["json"]:
                try:
                    with open(json_file) as f:
                        results[json_file.name] = json.load(f)
                except Exception as e:
                    if verbose:
                        print(f"Warning: Could not read {json_file.name}: {e}")

            return {
                "success": True,
                "output_dir": str(output_path),
                "files": files,
                "results": results,
                "stdout": stdout if verbose else None
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            Path(yaml_path).unlink(missing_ok=True)

    def extract_metrics(self, results: dict) -> dict:
        """Extract key metrics from BOLTZ results"""
        metrics = {}

        for filename, data in results.items():
            if "confidence" in filename and isinstance(data, dict):
                metrics.update({
                    "confidence_score": data.get("confidence_score", 0),
                    "ptm": data.get("ptm", 0),
                    "iptm": data.get("iptm", 0),
                    "plddt": data.get("complex_plddt", 0)
                })
            elif "affinity" in filename and isinstance(data, dict):
                # FIXED: Properly interpret affinity results
                # affinity_pred_value is log10(IC50 in μM) - this is what BOLTZ outputs
                log_ic50_uM = data.get("affinity_pred_value", 0)

                # Convert log10(IC50 in μM) to IC50 in μM
                ic50_uM = 10 ** log_ic50_uM

                # Convert to nM (1 μM = 1000 nM)
                ic50_nM = ic50_uM * 1000

                # Convert to M for proper pIC50 calculation
                ic50_M = ic50_uM * 1e-6

                # Calculate standard pIC50 (negative log of IC50 in molar units)
                # pIC50 = -log10(IC50 in M)
                pic50 = -np.log10(ic50_M) if ic50_M > 0 else 0

                # Calculate binding free energy in kcal/mol
                # Using the formula from BOLTZ documentation: (6 - affinity) * 1.364
                # Note: this assumes affinity_pred_value is in the range where 6 corresponds to 1 μM
                delta_g_kcal = (6 - log_ic50_uM) * 1.364

                # Approximate Kd from IC50 (Kd ≈ IC50/2 for competitive inhibitors)
                # This is a rough approximation!
                kd_uM = ic50_uM / 2
                kd_nM = kd_uM * 1000
                kd_M = kd_uM * 1e-6

                # Calculate pKd from Kd in molar units
                pkd = -np.log10(kd_M) if kd_M > 0 else 0

                metrics.update({
                    # Raw BOLTZ output
                    "boltz_affinity_value": log_ic50_uM,  # This is log10(IC50 in μM)

                    # IC50 values
                    "log_ic50_uM": log_ic50_uM,
                    "ic50_uM": ic50_uM,
                    "ic50_nM": ic50_nM,
                    "pic50": pic50,  # Standard pIC50

                    # Kd approximations
                    "kd_uM": kd_uM,
                    "kd_nM": kd_nM,
                    "pkd": pkd,

                    # Energy
                    "delta_g_kcal": delta_g_kcal,

                    # Binding probability
                    "affinity_prob": data.get("affinity_probability_binary", 0)
                })

        return metrics

# Initialize predictor
predictor = BOLTZPredictor()
#@title Visualization Functions

def visualize_structure(structure_path: Path, width: int = 800, height: int = 600):
    """Display 3D molecular structure"""

    with open(structure_path, 'r') as f:
        content = f.read()

    file_format = 'pdb' if str(structure_path).endswith('.pdb') else 'cif'

    view = py3Dmol.view(width=width, height=height)
    view.addModel(content, file_format)
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.setBackgroundColor('white')
    view.zoomTo()

    return view

def plot_confidence_distribution(plddt_file: Path) -> plt.Figure:
    """Plot per-residue confidence distribution"""

    data = np.load(plddt_file)
    plddt_values = data['plddt'] * 100  # Convert to percentage

    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram
    n, bins, patches = ax.hist(plddt_values, bins=50, alpha=0.7,
                               color='#2E86AB', edgecolor='black')

    # Color code by confidence level
    for i, patch in enumerate(patches):
        if bins[i] < 50:
            patch.set_facecolor('#D32F2F')  # Red - Very low
        elif bins[i] < 70:
            patch.set_facecolor('#F57C00')  # Orange - Low
        elif bins[i] < 90:
            patch.set_facecolor('#FBC02D')  # Yellow - Confident
        else:
            patch.set_facecolor('#388E3C')  # Green - High

    ax.axvline(plddt_values.mean(), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {plddt_values.mean():.1f}%')

    ax.set_xlabel('pLDDT Score (%)', fontsize=12)
    ax.set_ylabel('Number of Residues', fontsize=12)
    ax.set_title('Per-Residue Confidence Distribution', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig
