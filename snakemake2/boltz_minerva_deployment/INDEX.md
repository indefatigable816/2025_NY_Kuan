# HER2 Boltz Minerva Deployment Package - Index

**Generated**: December 4, 2025  
**Project**: HER2 isoform structure predictions with drug binding analysis  
**Target System**: Minerva HPC (MSSM)  
**Status**: Ready for deployment  

---

## 📁 Directory Structure

```
boltz_minerva_deployment/
│
├── 📖 DOCUMENTATION
│   ├── README.md                      ← Main guide (read first!)
│   ├── QUICK_START.md                 ← 5-minute setup guide
│   ├── EXECUTION_COMMANDS.md           ← Step-by-step command reference
│   ├── JOBS_MANIFEST.txt               ← Detailed job descriptions
│   └── INDEX.md                        ← This file
│
├── 🔧 CONFIGURATION & ORCHESTRATION
│   ├── Snakefile                      ← Snakemake workflow (optional)
│   └── submit_jobs_sequential.sh       ⭐ Main submission script (FAST)
│   └── submit_jobs_sequential_wait.sh  ← Alternative script (SAFE)
│
├── 📋 JOB SUBMISSION FILES (16 pairs)
│   ├── d16.lsf / d16.yaml
│   ├── d16_dimer.lsf / d16_dimer.yaml
│   ├── d16_trastuzumab.lsf / d16_trastuzumab.yaml
│   ├── K753E.lsf / K753E.yaml
│   ├── K753E_lapatinib.lsf / K753E_lapatinib.yaml
│   ├── L755S.lsf / L755S.yaml
│   ├── L755S_lapatinib.lsf / L755S_lapatinib.yaml
│   ├── S310F.lsf / S310F.yaml
│   ├── S310F_pertuzumab.lsf / S310F_pertuzumab.yaml
│   ├── WT_dimer.lsf / WT_dimer.yaml
│   ├── WT_ECD.lsf / WT_ECD.yaml
│   ├── WT_ICD.lsf / WT_ICD.yaml
│   ├── WT_lapatinib.lsf / WT_lapatinib.yaml
│   ├── WT_pertuzumab.lsf / WT_pertuzumab.yaml
│   └── WT_trastuzumab.lsf / WT_trastuzumab.yaml
│
├── 📁 configs/                        ← Additional configuration templates
└── 📁 scripts/                        ← Helper scripts directory
```

---

## 🚀 Quick Navigation

### For First-Time Users
1. **START HERE**: Read [`QUICK_START.md`](QUICK_START.md) (5 minutes)
2. **Then**: Read [`README.md`](README.md) (detailed overview)
3. **Reference**: Use [`EXECUTION_COMMANDS.md`](EXECUTION_COMMANDS.md) during actual execution

### For Understanding the Jobs
- **What jobs will run?** → See [`JOBS_MANIFEST.txt`](JOBS_MANIFEST.txt)
- **Detailed job breakdown?** → See [`README.md`](README.md) Job Information section

### For Running on Minerva
1. Copy folder: See [`EXECUTION_COMMANDS.md`](EXECUTION_COMMANDS.md) - Phase 1
2. Prepare files: See Phase 2
3. Submit jobs: See Phase 3 (choose Option A or B)
4. Monitor: See Phase 4
5. Get results: See Phase 6

### For Troubleshooting
- **Problem with jobs?** → See [`EXECUTION_COMMANDS.md`](EXECUTION_COMMANDS.md) Phase 7
- **Want to understand job details?** → See [`JOBS_MANIFEST.txt`](JOBS_MANIFEST.txt)
- **Need Minerva help?** → See [`README.md`](README.md) Contact & Support

---

## 📊 Project Summary

### Objective
Structure prediction and drug binding analysis for HER2 isoforms to identify novel therapeutic targets and resistance mechanisms.

### Jobs Overview
| Component | Count | Seeds | Total | Est. Time |
|-----------|-------|-------|-------|-----------|
| Monomers (ECD/ICD) | 6 | 10 | 60 | 4-12h each |
| Homodimers | 2 | 10 | 20 | 8-16h each |
| Drug Complexes | 8 | 10 | 80 | 12-24h each |
| **TOTAL** | **16** | **10** | **160** | **1-2 weeks** |

### HER2 Variants Included
- **Wild-type (WT)**: Reference structure
- **d16 (Δ16)**: Exon-16 deletion variant
- **K753E**: Kinase domain mutation
- **L755S**: Known lapatinib resistance mutation
- **S310F**: Potential pertuzumab escape variant

### Drug Molecules Included
- **Trastuzumab** (Herceptin): Monoclonal antibody against HER2 ECD
- **Pertuzumab** (Perjeta): Different epitope antibody, used in combination
- **Lapatinib**: Small-molecule kinase inhibitor (HER1/HER2)

---

## 📋 File Descriptions

### Documentation Files

| File | Purpose | Read Time | Key Info |
|------|---------|-----------|----------|
| `README.md` | Comprehensive guide with all details | 10-15 min | Setup, monitoring, troubleshooting |
| `QUICK_START.md` | Fast reference guide | 5 min | Copy-paste commands to get started |
| `EXECUTION_COMMANDS.md` | Complete command reference | 10-15 min | Every command you'll need, organized by phase |
| `JOBS_MANIFEST.txt` | Detailed job descriptions | 15-20 min | What each job does and why it matters |
| `INDEX.md` | This navigation guide | 5 min | Where to find what you need |

### Submission Files

| File Type | Count | Purpose |
|-----------|-------|---------|
| `.lsf` files | 16 | LSF batch submission scripts for Minerva |
| `.yaml` files | 16 | Boltz configuration files with protein sequences |

**Each pair (e.g., `d16.lsf` + `d16.yaml`) represents one job with 10 array seeds.**

### Execution Scripts

| Script | Type | Use Case | Speed | Safety |
|--------|------|----------|-------|--------|
| `submit_jobs_sequential.sh` | Shell script | Fast job submission | ⚡⚡⚡ FAST | ✓ Safe |
| `submit_jobs_sequential_wait.sh` | Shell script | Sequential with completion | ⚡ Slow | ✓✓ Safer |
| `Snakefile` | Snakemake | Local orchestration | Variable | Optional |

---

## ⚡ Quick Command Reference

### Transfer to Minerva (Local Machine - PowerShell)
```powershell
scp -r boltz_minerva_deployment cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/
```

### Prepare on Minerva (Minerva Terminal)
```bash
cd /sc/arion/work/cheny69/boltz_minerva_deployment
cp *.lsf *.yaml /sc/arion/work/cheny69/1216/
chmod +x *.sh
```

### Submit Jobs (Choose ONE)
```bash
# Option A: Fast submission (recommended)
./submit_jobs_sequential.sh

# Option B: Sequential with waiting
./submit_jobs_sequential_wait.sh
```

### Monitor
```bash
bjobs                  # See all jobs
bjobs -a               # See completed jobs
bhist | head -20       # Job history
```

### Get Results
```bash
find /sc/arion/work/cheny69/1216/results -name "*_model_*.cif" | wc -l
```

---

## 🗂️ Generated Outputs (After Completion)

Results will be organized as:
```
/sc/arion/work/cheny69/1216/results/
├── monomer/
│   ├── ECD/         ← d16, WT_ECD, S310F
│   └── molecule/    ← WT_ICD, K753E, L755S
└── multimer/
    ├── WT_dimer/, d16_dimer/              ← Dimers
    ├── WT_trastuzumab/, d16_trastuzumab/  ← Trastuzumab complexes
    ├── WT_pertuzumab/, S310F_pertuzumab/  ← Pertuzumab complexes
    └── WT_lapatinib/, K753E_lapatinib/, L755S_lapatinib/  ← Lapatinib complexes
```

Each job's results include:
- `*_model_1.cif` - Predicted 3D structure
- `confidence_model_1.json` - Quality scores (pLDDT, PAE)
- `plddt_*.npz` - Per-residue confidence
- `pae_*.npz` - Predicted alignment error matrix

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ All 16 job submission files copied to Minerva  
✅ Both `.lsf` and `.yaml` files present for each job  
✅ Submission script runs without errors  
✅ All 16 jobs appear in `bjobs` output  
✅ Results directories created in `/sc/arion/work/cheny69/1216/results/`  
✅ After 1-2 weeks: 160 structure files generated (one per seed)  

---

## 📞 Support & References

### Minerva Documentation
- **General**: https://labs.icahn.mssm.edu/minervalab/
- **LSF Job Scheduler**: https://labs.icahn.mssm.edu/minervalab/documentation/lsf-job-scheduler/
- **GPU Setup**: https://labs.icahn.mssm.edu/minervalab/documentation/gpgpu/
- **Conda**: https://labs.icahn.mssm.edu/minervalab/documentation/conda/

### Boltz Documentation
- **GitHub**: https://github.com/jwohlwend/boltz
- **Prediction Guide**: https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md
- **Model Details**: See Boltz papers and documentation

### Common Issues
See "Troubleshooting" section in [`README.md`](README.md) or Phase 7 in [`EXECUTION_COMMANDS.md`](EXECUTION_COMMANDS.md)

---

## 📝 File Checklist

Before deployment, verify you have:

**Documentation** (5 files)
- [ ] README.md
- [ ] QUICK_START.md
- [ ] EXECUTION_COMMANDS.md
- [ ] JOBS_MANIFEST.txt
- [ ] INDEX.md (this file)

**Scripts** (3 files)
- [ ] Snakefile
- [ ] submit_jobs_sequential.sh
- [ ] submit_jobs_sequential_wait.sh

**Configuration Files** (32 files)
- [ ] 16 × `.lsf` files
- [ ] 16 × `.yaml` files

**Directories** (2 directories)
- [ ] configs/
- [ ] scripts/

**Total: 5 docs + 3 scripts + 32 config files + 2 directories = ✓ Complete Package**

---

## 🔄 Workflow Timeline

```
Day 0
├─ Transfer folder to Minerva (2 min)
├─ Copy files to 1109 directory (1 min)
└─ Submit all jobs (2 min) ← YOU ARE HERE AFTER QUICK_START
        ↓
        ↓ (GPU queue processes jobs)
        ↓
Days 1-14
├─ Monitor job progress (bjobs)
└─ As jobs complete, results populate
        ↓
Day 14+ (when all complete)
├─ Create archive of results
├─ Download to your machine
└─ Analyze structures (PyMOL, ChimeraX, etc.)
```

---

## 💾 Storage Notes

- **Local disk used**: ~500GB (16 jobs × 10 seeds × 3GB average)
- **Minerva location**: `/sc/arion/work/cheny69/1216/` (better storage than `/hpc/users/`)
- **Archive size**: ~150-200GB (compressed results)
- **Download time**: ~1-2 hours (depends on network and file size)

---

## 🎓 Learning Resources

### Understanding the Project
- Read: `README.md` - Project Overview section
- Read: `JOBS_MANIFEST.txt` - Job descriptions with scientific context

### Understanding Boltz
- Check: [Boltz GitHub](https://github.com/jwohlwend/boltz)
- Check: Original Boltz papers (cited in Boltz documentation)

### Understanding LSF & Minerva
- Check: [Minerva LSF Documentation](https://labs.icahn.mssm.edu/minervalab/documentation/lsf-job-scheduler/)
- Check: Example LSF files in this package (look at any `.lsf` file)

---

## 📌 Important Reminders

1. **Do NOT submit all jobs manually** - use the provided scripts
2. **GPU environment is shared** - sequential submission prevents overload
3. **Conda env (boltz0929) is pre-configured** - no need to install dependencies
4. **MSA server requires internet** - Minerva has this configured
5. **Jobs take 1-2 weeks** - be patient, check status regularly
6. **Results are large** - plan storage before downloading

---

## 📊 Version Info

| Component | Version |
|-----------|---------|
| Deployment Package | 1.0 |
| Boltz Framework | 2.2.0 |
| Python Requirements | 3.10-3.12 |
| Target Conda Env | boltz0929 |
| Minerva Location | `/sc/arion/work/cheny69/` |

---

## ✨ What's Included

✅ **Complete LSF/YAML configuration** for all 16 jobs  
✅ **Two submission strategies** (fast & safe options)  
✅ **Comprehensive documentation** (5 guides)  
✅ **Real-time monitoring instructions**  
✅ **Troubleshooting guide**  
✅ **Result retrieval workflow**  
✅ **Example commands** for every step  

---

**Status**: ✅ Ready to Deploy  
**Next Step**: Read [`QUICK_START.md`](QUICK_START.md)  
**Questions**: See [`README.md`](README.md) or [`EXECUTION_COMMANDS.md`](EXECUTION_COMMANDS.md)  

---

*Generated: December 4, 2025 | Project: NY HER2 Isoform Analysis*
