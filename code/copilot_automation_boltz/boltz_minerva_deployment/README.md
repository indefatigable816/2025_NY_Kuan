# HER2 Boltz Predictions on Minerva - Deployment Guide

This directory contains everything needed to run sequential HER2 boltz structure predictions on the Minerva HPC cluster.

## Project Overview

**Objective**: Run Boltz structural predictions for:
- HER2 monomers (ECD/ICD) with various isoforms and mutations
- HER2 multimers (dimers and drug-binding complexes)
- Analysis of trastuzumab, pertuzumab, and lapatinib binding

**Total Jobs**: 15 prediction jobs (each with 10 seeds = 150 total GPU array jobs)

## Directory Contents

```
boltz_minerva_deployment/
├── Snakefile                          # Snakemake workflow (optional, for local orchestration)
├── submit_jobs_sequential.sh           # Main submission script (RECOMMENDED)
├── submit_jobs_sequential_wait.sh      # Alternative with job completion waiting
├── *.lsf                               # LSF job submission files (16 total)
├── *.yaml                              # Sequence configuration files (16 total)
├── README.md                           # This file
├── QUICK_START.md                      # Quick reference guide
├── JOBS_MANIFEST.txt                   # Detailed job descriptions
└── configs/                            # Configuration templates (if needed)
```

## Quick Start

### On Your Local Machine

```powershell
# Copy the entire boltz_minerva_deployment directory to Minerva
scp -r C:\Users\indef\Documents\NY\project\snakemake\boltz_minerva_deployment cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/
```

### On Minerva Terminal

```bash
# 1. Navigate to the deployment directory
cd /sc/arion/work/cheny69/boltz_minerva_deployment

# 2. Copy LSF and YAML files to the 1216 working directory
cp *.lsf *.yaml /sc/arion/work/cheny69/1216/

# 3. Make submission script executable
chmod +x submit_jobs_sequential.sh

# 4. Submit jobs (choose one option below)

# Option A: Submit jobs immediately (recommended for efficiency)
./submit_jobs_sequential.sh

# Option B: Submit jobs and wait for each to complete
./submit_jobs_sequential_wait.sh

# 5. Monitor job progress
bjobs                    # View all your jobs
bjobs -a                 # Include finished jobs
bjobs -l <JOB_ID>       # Detailed info on specific job
bhist                    # View job history
```

## Job Submission Details

### Option 1: Fast Sequential Submission (Recommended)

**Script**: `submit_jobs_sequential.sh`

- Submits all 15 jobs quickly (one every 5 seconds)
- Returns immediately, allowing you to disconnect
- GPU environment handles queue scheduling
- Logs submissions for reference
- **Use this if**: You want jobs to start running quickly

**Example Output**:
```
[1/15] Submitting d16...
  ✓ Job ID: 1234567
  Waiting 5 seconds before next submission...
[2/15] Submitting WT_ECD...
  ✓ Job ID: 1234568
  ...
```

### Option 2: Sequential with Completion Waiting

**Script**: `submit_jobs_sequential_wait.sh`

- Submits a job, waits for it to complete, then submits the next
- Prevents all 16 array jobs from running simultaneously
- More conservative, uses GPU resources sequentially
- Takes longer overall but safer for environment stability
- **Use this if**: You want guaranteed sequential execution

## Job Information

### Job Categories

#### Monomer Predictions (6 jobs)
- **d16**: Delta-16 HER2 isoform (ECD)
- **WT_ECD**: Wild-type HER2 extracellular domain
- **S310F**: S310F mutation (ECD)
- **WT_ICD**: Wild-type HER2 intracellular domain
- **K753E**: K753E mutation (intracellular)
- **L755S**: L755S mutation (intracellular)

#### Multimer Predictions (10 jobs)

**Dimers** (2 jobs):
- **WT_dimer**: Wild-type HER2 homodimer
- **d16_dimer**: Delta-16 HER2 homodimer

**Trastuzumab Complexes** (2 jobs):
- **WT_trastuzumab**: WT HER2 + trastuzumab Fab
- **d16_trastuzumab**: d16 HER2 + trastuzumab Fab

**Pertuzumab Complexes** (2 jobs):
- **WT_pertuzumab**: WT HER2 + pertuzumab Fab
- **S310F_pertuzumab**: S310F HER2 + pertuzumab Fab

**Lapatinib Complexes** (3 jobs):
- **WT_lapatinib**: WT HER2 + lapatinib ligand
- **K753E_lapatinib**: K753E HER2 + lapatinib ligand
- **L755S_lapatinib**: L755S HER2 + lapatinib ligand

### Array Job Structure

Each `.lsf` file defines an array job with 10 seeds:
```
#BSUB -J JOB_NAME[1-10]
```

This creates 10 independent predictions with different random seeds for increased sampling.

## Monitoring and Troubleshooting

### Check Job Status

```bash
# List all your jobs
bjobs

# Show detailed information for a job
bjobs -l 1234567

# View job history
bhist | head -20

# Check GPU utilization
gpustat              # If available
nvidia-smi           # Check GPU status
```

### Common Issues

#### Job stays in PEND (pending) status
```bash
# Check available GPUs
bhosts -gpu

# Check queue status
bqueues

# Your project might not have GPU allocation - ask your PI to add you to the project
```

#### Job fails or errors
```bash
# Check error logs
ls -la /sc/arion/work/cheny69/1216/err.*

# View specific error log
cat /sc/arion/work/cheny69/1216/err.JOBID.SEED
```

#### Memory issues
- Multimer predictions (especially drug complexes) need more memory
- Current LSF config allocates up to 200GB for large jobs
- If you get OOM errors, check the `.lsf` file's `-R rusage[mem=...]` parameter

### Retrieve Results

```bash
# Navigate to results directory
cd /sc/arion/work/cheny69/1216/results

# Find all model output files
find . -name "*_model_*.cif" | head -10

# Create a compressed archive of results
find . -type f \( -name '*_model_*.cif' -o -name 'confidence_*.json' -o -name '*_*.csv' \) \
    -print0 | tar --null -czf results_needed.tar.gz --files-from=-

# Copy back to your machine
scp cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/1216/results_needed.tar.gz .
```

## Snakemake Workflow (Advanced)

If you prefer to use Snakemake for local orchestration on your machine:

```bash
# Install Snakemake (if not already installed)
pip install snakemake

# Validate the workflow
snakemake --snakefile Snakefile --dry-run

# Run (will create local logs, not actually submit to Minerva)
snakemake --snakefile Snakefile
```

Note: The Snakefile is included for reference but the shell scripts are the primary submission method.

## Important Notes

### GPU Environment Protection
- **Do NOT submit all 15 jobs at once** (unless you have explicit approval)
- Each job uses array syntax `[1-10]`, creating 10 parallel GPU jobs per submission
- Running all 15 simultaneously = 150 GPU jobs = environment overload
- Both submission scripts respect this by spreading submissions over time

### QC Criteria and Automated Check

- **QC Criteria**: By project policy, a prediction is considered acceptable when `ptm > 0.5` and `iptm > 0.3`.
- For each job we require at least **10 passing predictions** (i.e. 10 seeds meeting the criteria). If fewer than 10 pass, the job should be re-run (or additional seeds should be generated) until the threshold is met.
- A small helper script is provided to summarize QC and suggest resubmission steps:

  - Script: `scripts/qc_check_and_resubmit.py`
  - Example (run on Minerva after a job completes):

    python3 scripts/qc_check_and_resubmit.py \
      --results-dir /sc/arion/work/cheny69/1216/results \
      --job-name WT_trastuzumab \
      --min-pass 10

  - The script writes `qc_report.txt` and, when resubmission is needed, `resubmit_instructions.txt` with suggested commands and tips for creating a resubmit `.lsf`.

  - The script is intentionally conservative: it reports and suggests actions rather than auto-resubmitting. This keeps submissions under your control and avoids accidental overload.

### Storage Location
- Working directory: `/sc/arion/work/cheny69/1216/`
  - Better storage allocation than `/hpc/users/cheny69/`
  - As specified in your convenience.md

### Conda Environment
- Uses `boltz0929` environment (pre-configured)
- Located at: `/sc/arion/work/cheny69/boltz0929/`
- All dependencies pre-installed per pyproject.toml

### MSA Server
- All jobs use `--use_msa_server` flag
- Requires internet access (configured via `ml proxies/1`)
- Can be slow if many jobs compete for MSA data
- Sequential submission helps mitigate this

## File Mappings

### Configuration Files (LSF Headers)
```
Example from d16.lsf:
#BSUB -P acc_DiseaseGeneCell        # Project for GPU queue
#BSUB -J HER2[1-20]                 # Job array: 1-10 seeds
#BSUB -q gpu                        # GPU queue
#BSUB -R rusage[mem=100000]         # Memory allocation
#BSUB -W 24:00                      # Wall time (24 hours)
```

### Sequence Files (YAML Structure)
```yaml
version: 1
sequences:
  - protein:
      id: D                # Protein identifier
      sequence: TQVCTG... # Amino acid sequence
```

For multimer/drug complexes:
```yaml
sequences:
  - protein:
      id: A               # First protein
      sequence: ...
  - ligand:
      id: B               # Drug or protein
      smiles: ...         # Chemical structure
properties:
  - affinity:
      binder: B           # Ligand ID
```

## Contact & Support

For Minerva-specific issues:
- Minerva docs: https://labs.icahn.mssm.edu/minervalab/
- LSF docs: https://labs.icahn.mssm.edu/minervalab/documentation/lsf-job-scheduler/
- GPU docs: https://labs.icahn.mssm.edu/minervalab/documentation/gpgpu/

For Boltz-specific questions:
- Boltz GitHub: https://github.com/jwohlwend/boltz
- Boltz docs: https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md

## Timeline Estimates

**Job Submission Time**: ~2 minutes (fast script) or ~30-60 minutes (wait script)

**Expected Computation Time** (per array job with 10 seeds):
- Monomer predictions: 4-8 hours
- Dimer predictions: 8-16 hours  
- Drug-binding complexes: 12-24 hours

**Total Expected Timeline**: 7-14 days for all 16 jobs to complete (depends on GPU queue)

---

**Last Updated**: December 4, 2025
**Deployment Version**: 1.0
