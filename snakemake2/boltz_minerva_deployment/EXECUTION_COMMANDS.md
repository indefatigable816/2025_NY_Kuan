# Minerva Execution Commands - Step by Step

## PHASE 1: TRANSFER & SETUP (Local Machine)

### Copy deployment folder to Minerva

**On your Windows machine (PowerShell):**

```powershell
# Navigate to your project directory
cd C:\Users\indef\Documents\NY\project\snakemake

# Option 1: Copy the entire deployment folder
scp -r boltz_minerva_deployment cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/

# Verify transfer completed (should see no errors)
echo "Transfer complete!"
```

**Expected output:**
```
Deployment folder and all files copied...
```

---

## PHASE 2: PREPARE ON MINERVA (Minerva Terminal)

### Step 1: Connect to Minerva

```bash
ssh cheny69@minerva.hpc.mssm.edu
```

### Step 2: Navigate to deployment folder

```bash
cd /sc/arion/work/cheny69/boltz_minerva_deployment
ls -la
```

**You should see:**
```
Snakefile
submit_jobs_sequential.sh
submit_jobs_sequential_wait.sh
README.md
QUICK_START.md
JOBS_MANIFEST.txt
d16.lsf
d16.yaml
d16_dimer.lsf
... (all 16 .lsf and .yaml files)
```

### Step 3: Copy configuration files to working directory

```bash
cp *.lsf *.yaml /sc/arion/work/cheny69/1216/
cd /sc/arion/work/cheny69/1216
ls -la *.lsf *.yaml | wc -l
```

**Expected output:**
```
32
```

(16 LSF files + 16 YAML files = 32 total)

### Step 4: Make submission scripts executable

```bash
cd /sc/arion/work/cheny69/boltz_minerva_deployment
chmod +x submit_jobs_sequential.sh
chmod +x submit_jobs_sequential_wait.sh
ls -la *.sh
```

**Expected output:**
```
-rwxr-xr-x  1  cheny69  domain users  ...  submit_jobs_sequential.sh
-rwxr-xr-x  1  cheny69  domain users  ...  submit_jobs_sequential_wait.sh
```

---

## PHASE 3: SUBMIT JOBS (Choose ONE option)

### ⭐ OPTION A: FAST SEQUENTIAL SUBMISSION (RECOMMENDED)

**Use this if you want jobs to start quickly without waiting for completion.**

```bash
cd /sc/arion/work/cheny69/boltz_minerva_deployment
./submit_jobs_sequential.sh
```

**What happens:**
- Submits all 16 jobs over ~2 minutes
- Each job gets a job ID
- Script returns immediately
- You can disconnect safely

**Expected output:**
```
==========================================
HER2 Boltz Sequential Job Submission
==========================================
Working Directory: /sc/arion/work/cheny69/1216
Log Directory: /sc/arion/work/cheny69/1216/submission_logs
Submission Start: 2025-12-04_14-32-15

Total jobs to submit: 15

[1/15] Submitting d16...
  ✓ Job ID: 1234567
  Waiting 5 seconds before next submission...
[2/15] Submitting WT_ECD...
  ✓ Job ID: 1234568
  Waiting 5 seconds before next submission...
... (continues for all 16 jobs) ...

==========================================
Submission Summary
==========================================
Total jobs submitted: 16
Total jobs failed: 0
Submission End: Wed Dec  4 14:34:30 EST 2025

Submission Log: /sc/arion/work/cheny69/1216/submission_logs/submissions_2025-12-04_14-32-15.log
```

### OPTION B: SEQUENTIAL WITH COMPLETION WAITING

**Use this if you want true sequential execution (safer but slower overall).**

```bash
cd /sc/arion/work/cheny69/boltz_minerva_deployment
./submit_jobs_sequential_wait.sh
```

**What happens:**
- Submits job #1, waits for completion
- Then submits job #2, waits for completion
- Repeats for all 16 jobs
- Takes 7-14 days total
- More conservative GPU usage

**Note:** Running this in background is recommended:

```bash
nohup ./submit_jobs_sequential_wait.sh > submission.log 2>&1 &
echo $!  # Save this process ID
```

---

## PHASE 4: MONITOR JOB PROGRESS

### Real-time Job Status

```bash
# List all your active jobs
bjobs

# List all jobs including finished ones
bjobs -a

# Very detailed info on a specific job
bjobs -l 1234567

# View job history (most recent first)
bhist | head -20

# Check queue status
bqueues

# Check GPU availability
bhosts -gpu
```

### Check Specific Job Details

```bash
# Get job stats (runtime, status, host)
bjobs -l <JOB_ID>

# View job log files while running
tail -f /sc/arion/work/cheny69/1216/out.<JOB_ID>.<SEED>
tail -f /sc/arion/work/cheny69/1216/err.<JOB_ID>.<SEED>
```

### Monitor Results Generation

```bash
# Count completed prediction files
find /sc/arion/work/cheny69/1216/results -name "*_model_*.cif" | wc -l

# Watch results appearing in real-time
watch -n 60 'find /sc/arion/work/cheny69/1216/results -name "*_model_*.cif" | wc -l'

# Check if specific job is done
ls -la /sc/arion/work/cheny69/1216/results/multimer/WT_trastuzumab/1/
```

---

## PHASE 5: MANAGE RUNNING JOBS

### Pause/Resume Jobs

```bash
# Suspend a job (job stays in queue)
bstop <JOB_ID>

# Resume suspended job
bresume <JOB_ID>
```

### Cancel Jobs

```bash
# Cancel one specific job
bkill <JOB_ID>

# Cancel all your jobs
bkill 0

# Cancel jobs by status
bkill -u cheny69 -b  # Only pending jobs
```

### Check Completion Status

```bash
# Check if all 15 jobs have completed
bjobs -a | grep "d16 \|WT_ECD\|S310F\|WT_ICD\|K753E\|L755S\|WT_dimer\|d16_dimer\|WT_tras\|d16_tras\|WT_pert\|S310F_pert\|WT_lapa\|K753E_lapa\|L755S_lapa"

# See only completed jobs
bjobs -a | grep "DONE"

# See failed jobs
bjobs -a | grep "EXIT"
```

---

## PHASE 6: RETRIEVE RESULTS

### While Jobs Are Still Running

```bash
# Check results directory structure
du -sh /sc/arion/work/cheny69/1216/results/

# Count output files generated so far
find /sc/arion/work/cheny69/1216/results -type f | wc -l

# View results from a completed job
ls /sc/arion/work/cheny69/1216/results/monomer/ECD/d16/1/
```

### After All Jobs Complete

```bash
# Verify all 150 prediction files exist (15 jobs × 10 seeds)
find /sc/arion/work/cheny69/1216/results -name "*_model_*.cif" | wc -l
# Should output: 150

# Create compressed archive of all results
cd /sc/arion/work/cheny69/1216
find . -type f \( \
    -name '*_model_*.cif' \
    -o -name 'confidence_*.json' \
    -o -name 'plddt_*.npz' \
    -o -name 'pae_*.npz' \
    -o -name '*.csv' \
) -print0 | tar --null -czf results_complete.tar.gz --files-from=-

# Verify archive
tar -tzf results_complete.tar.gz | head -20
```

### Download Results to Your Machine

**On your Windows machine:**

```powershell
# Download the results archive
scp cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/1216/results_complete.tar.gz .

# Extract locally
tar -xzf results_complete.tar.gz

# Or, just view directory structure remotely first
ssh cheny69@minerva.hpc.mssm.edu "du -sh /sc/arion/work/cheny69/1216/results/*"
```

---

## PHASE 7: TROUBLESHOOTING

### Job Won't Start (PEND status)

```bash
# Check why it's pending
bjobs -l <JOB_ID>

# Look for "REASON" field - common issues:

# 1. No GPU available
bhosts -gpu | grep gpu

# 2. You're not in a project
bsub -P acc_DiseaseGeneCell  # Ask your PI to add you

# 3. Queue is full
bqueues

# 4. Memory limit exceeded
# Edit the .lsf file: -R rusage[mem=XXX]
nano /sc/arion/work/cheny69/1216/WT_trastuzumab.lsf
```

### Job Crashes or Errors

```bash
# Check error logs
ls /sc/arion/work/cheny69/1216/err.*

# View specific error
cat /sc/arion/work/cheny69/1216/err.1234567.5

# Check if it's an MSA server issue (try resubmitting)
bkill <JOB_ID>
sleep 30
bsub < /sc/arion/work/cheny69/1216/WT_trastuzumab.lsf

# Check system resources during job run
# (Run this in another terminal while job is running)
bhosts -gpu
top -u cheny69
```

### Out of Memory (OOM)

```bash
# Current memory allocation in d16.lsf:
grep "rusage\[mem" /sc/arion/work/cheny69/1216/d16.lsf
# Output: #BSUB -R rusage[mem=100000]

# Increase for all jobs:
for f in /sc/arion/work/cheny69/1216/*.lsf; do
  sed -i 's/rusage\[mem=[0-9]*\]/rusage[mem=256000]/g' "$f"
done

# Verify change
grep "rusage\[mem" /sc/arion/work/cheny69/1216/*.lsf | head -3
```

### Check Submission Log

```bash
# View your submission log
cat /sc/arion/work/cheny69/1216/submission_logs/submissions_*.log

# See which jobs submitted and when
tail -50 /sc/arion/work/cheny69/1216/submission_logs/submissions_*.log
```

---

## PHASE 8: FINAL CLEANUP & RESULTS

### Once Everything Is Complete

```bash
# Verify all output files
find /sc/arion/work/cheny69/1216/results -name "*_model_*.cif" | wc -l
# Should be: 150

# Check job history
bhist | grep "HER2" | head -20

# View statistics
bhist -l | tail -20
```

### Prepare Final Archive

```bash
# cd to working directory
cd /sc/arion/work/cheny69/1216

# Create summary of what completed
find results -name "*_model_*.cif" | sort > COMPLETED_PREDICTIONS.txt

# Create metadata file
cat > RESULTS_METADATA.txt << 'EOF'
HER2 Boltz Predictions - Completion Summary
Generated: $(date)

Total jobs submitted: 15
Expected predictions per job: 10 (array job with seeds 1-10)
Total expected predictions: 150

Prediction categories:
- Monomers (ECD/ICD): 6 jobs × 10 seeds = 60 predictions
- Dimers: 2 jobs × 10 seeds = 20 predictions  
- Drug complexes: 8 jobs × 10 seeds = 80 predictions

Results location: /sc/arion/work/cheny69/1216/results/
EOF

# Create final archive with everything
tar -czf HER2_BOLTZ_RESULTS_FINAL.tar.gz \
    results/ \
    COMPLETED_PREDICTIONS.txt \
    RESULTS_METADATA.txt

# Show size
du -sh HER2_BOLTZ_RESULTS_FINAL.tar.gz
```

### Download Final Archive

```powershell
# On your Windows machine
scp cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/1216/HER2_BOLTZ_RESULTS_FINAL.tar.gz .

# Extract
tar -xzf HER2_BOLTZ_RESULTS_FINAL.tar.gz

# Verify contents
ls -la results/
```

---

## Quick Reference: Command Cheat Sheet

```bash
# Monitor jobs
bjobs                          # All active jobs
bjobs -a                       # All jobs (active + done)
bhist                          # Job history

# Check status
bjobs -l <JOB_ID>              # Detailed info
bhosts -gpu                    # GPU availability
bqueues                        # Queue status

# Control jobs
bstop <JOB_ID>                 # Suspend
bresume <JOB_ID>               # Resume
bkill <JOB_ID>                 # Cancel

# View logs
tail -f err.JOBID.SEED         # Watch errors
tail -f out.JOBID.SEED         # Watch output

# Check results
find results -name "*_model_*.cif" | wc -l  # Count predictions
du -sh results/                # Total size
```

---

**Estimated Total Runtime: 7-14 days from submission to completion**

For detailed information, see `README.md` and `JOBS_MANIFEST.txt`
