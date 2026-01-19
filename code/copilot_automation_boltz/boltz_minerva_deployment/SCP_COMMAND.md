# SCP Command - Ready to Copy & Paste

## For Your PowerShell Terminal

### Single Command to Transfer Everything

```powershell
scp -r C:\Users\indef\Documents\NY\project\snakemake\boltz_minerva_deployment cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/
```

**That's it! Copy the command above, paste it in PowerShell, and run.**

---

## What This Command Does

1. Transfers the entire `boltz_minerva_deployment` folder
2. Copies all 39 files (docs, scripts, configs)
3. Preserves directory structure
4. Uses secure SSH connection (scp = secure copy)
5. Saves to Minerva at: `/sc/arion/work/cheny69/boltz_minerva_deployment/`

---

## Expected Output

```
d16.lsf                                      100%   684     2.1 MB/s   00:00
d16.yaml                                     100%   709     2.2 MB/s   00:00
d16_dimer.lsf                                100%   693     2.1 MB/s   00:00
... (continues for all 39 files) ...
Snakefile                                    100%  2187     6.7 MB/s   00:00
```

**When done**, you should see:
```
PS C:\Users\indef\Documents\NY\project\snakemake> 
```

---

## Alternative: If You Prefer Step-by-Step

### Transfer just the deployment folder
```powershell
scp -r C:\Users\indef\Documents\NY\project\snakemake\boltz_minerva_deployment `
  cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/
```

### Then SSH and verify
```bash
ssh cheny69@minerva.hpc.mssm.edu
ls -la /sc/arion/work/cheny69/boltz_minerva_deployment/
```

---

## Common Issues & Solutions

### "scp: command not found"
**Solution**: Windows 10+ has scp built-in. If missing:
- Use a different terminal (WSL, Git Bash, or download putty)
- Or use `pscp` from PuTTY: `pscp -r C:\path... user@minerva.hpc.mssm.edu:/path/`

### "Permission denied (publickey)"
**Solution**: Make sure you're using the correct username:
- Should be: `cheny69@minerva.hpc.mssm.edu`
- Have your password ready

### "Host key not verified"
**Solution**: Type `yes` when asked if you trust the connection

### Transfer takes a long time
**Solution**: Normal! 39 files, all encrypted. Should take 30 seconds to 2 minutes.

---

## Verification After Transfer

On Minerva, verify the transfer:

```bash
# List the transferred folder
ls -la /sc/arion/work/cheny69/boltz_minerva_deployment/

# Count files
find /sc/arion/work/cheny69/boltz_minerva_deployment -type f | wc -l
# Should show: 39 files

# Verify config files
ls /sc/arion/work/cheny69/boltz_minerva_deployment/*.lsf | wc -l
# Should show: 16

ls /sc/arion/work/cheny69/boltz_minerva_deployment/*.yaml | wc -l
# Should show: 16
```

---

## Next Steps After Transfer

Once transfer is complete, on your Minerva terminal:

```bash
# Navigate to deployment folder
cd /sc/arion/work/cheny69/boltz_minerva_deployment

# Copy configuration files to working directory
cp *.lsf *.yaml /sc/arion/work/cheny69/1216/

# Make scripts executable
chmod +x *.sh

# Submit jobs (choose one)
./submit_jobs_sequential.sh          # Fast (recommended)
# OR
./submit_jobs_sequential_wait.sh     # Safe (waits for completion)
```

---

## Copy-Paste Ready Commands

### PowerShell (Local Machine)
```powershell
scp -r C:\Users\indef\Documents\NY\project\snakemake\boltz_minerva_deployment cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/
```

### Minerva Terminal (After Transfer)
```bash
cd /sc/arion/work/cheny69/boltz_minerva_deployment
cp *.lsf *.yaml /sc/arion/work/cheny69/1216/
chmod +x *.sh
./submit_jobs_sequential.sh
```

---

## Files Being Transferred (39 total)

### Documentation (8 files)
- START_HERE.md
- DEPLOYMENT_SUMMARY.md
- INDEX.md
- QUICK_START.md
- README.md
- EXECUTION_COMMANDS.md
- JOBS_MANIFEST.txt
- SCP_COMMAND.md (this file)

### Scripts (2 files)
- Snakefile
- submit_jobs_sequential.sh
- submit_jobs_sequential_wait.sh

### Config Files (32 files)
- d16.lsf, d16.yaml
- d16_dimer.lsf, d16_dimer.yaml
- d16_trastuzumab.lsf, d16_trastuzumab.yaml
- K753E.lsf, K753E.yaml
- K753E_lapatinib.lsf, K753E_lapatinib.yaml
- L755S.lsf, L755S.yaml
- L755S_lapatinib.lsf, L755S_lapatinib.yaml
- S310F.lsf, S310F.yaml
- S310F_pertuzumab.lsf, S310F_pertuzumab.yaml
- WT_dimer.lsf, WT_dimer.yaml
- WT_ECD.lsf, WT_ECD.yaml
- WT_ICD.lsf, WT_ICD.yaml
- WT_lapatinib.lsf, WT_lapatinib.yaml
- WT_pertuzumab.lsf, WT_pertuzumab.yaml
- WT_trastuzumab.lsf, WT_trastuzumab.yaml

### Directories (2)
- configs/
- scripts/

---

## Important Notes

✅ **Secure**: Uses SSH encryption  
✅ **Complete**: All files transferred automatically  
✅ **Resumable**: Can rerun if connection drops  
✅ **No mods needed**: Files are ready to use  

---

**Ready?** Just copy the command at the top and paste it in PowerShell!
