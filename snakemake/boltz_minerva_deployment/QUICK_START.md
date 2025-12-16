# Quick Start Guide - 5 Minutes to Running

## Step 1: Copy to Minerva (2 min)

On your local machine (PowerShell):
```powershell
scp -r C:\Users\indef\Documents\NY\project\snakemake\boltz_minerva_deployment cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/
```

## Step 2: Prepare Files on Minerva (1 min)

SSH into Minerva:
```bash
ssh cheny69@minerva.hpc.mssm.edu

# Navigate and prepare
cd /sc/arion/work/cheny69/boltz_minerva_deployment
cp *.lsf *.yaml /sc/arion/work/cheny69/1216/
chmod +x *.sh
```

## Step 3: Submit Jobs (1 min)

**Option A - Fast (recommended)**:
```bash
./submit_jobs_sequential.sh
```

**Option B - Safe (waits for completion)**:
```bash
./submit_jobs_sequential_wait.sh
```

## Step 4: Monitor (1 min)

```bash
# Check jobs
bjobs

# Detailed view
bjobs -a

# Job history
bhist | head -20
```

---

## That's it! Jobs are running.

## While Jobs Run

You can safely close your terminal. Jobs will continue.

Check status anytime:
```bash
ssh cheny69@minerva.hpc.mssm.edu
bjobs
```

## Get Results

When done (in ~1-2 weeks):
```bash
cd /sc/arion/work/cheny69/1216/results
find . -name "*_model_*.cif" -o -name "*.json" | wc -l  # Count outputs
```

Create archive:
```bash
find . -type f \( -name '*_model_*.cif' -o -name 'confidence_*.json' \) \
    -print0 | tar --null -czf results.tar.gz --files-from=-
```

Download to your machine:
```powershell
scp cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/1216/results.tar.gz .
tar -xzf results.tar.gz
```

---

## Troubleshooting

**Job stuck in PEND?**
```bash
bqueues              # Check queue status
bjobs -l JOBID       # See why it's pending
```

**Need to cancel jobs?**
```bash
bkill JOBID          # Cancel one job
bkill 0              # Cancel all your jobs
```

**Check errors?**
```bash
ls -la /sc/arion/work/cheny69/1216/err.*
cat err.JOBID.SEED
```

---

For detailed info, see `README.md`
