Protocol:
https://docs.google.com/document/d/1PTOMLRsIBdl5XNer5PmSpld-OnheUxNBB3auJ8sFSp8/edit?tab=t.0#heading=h.z6dcsim9vf3y
Next step:
## Your Original Intention

You set out to design **new antibody-based therapeutics** that can overcome resistance to current HER2-targeted drugs (trastuzumab/pertuzumab). Specifically:

1. **Identify neo-epitopes** - Find unique surface features on resistant isoforms (especially Δ16HER2/p95HER2) that differ from wild-type
2. **Design isoform-selective antibodies** - Create antibodies that specifically target the resistant variants
3. **Explore new modalities** - Consider ADCs, bispecifics (e.g., Δ16HER2 × CD3), or Fc-engineered variants

## Your Next Step: Week 4 - Model Validation & Complex Building

You should now:

### 1. **Build Drug-Isoform Complexes**
- Model how **trastuzumab** and **pertuzumab** bind (or fail to bind) to each of your isoforms
- Use either:
  - AlphaFold-3 multimer mode (drug Fab + isoform)
  - Boltz2 docking (your protocol mentions this specifically)
- Target: `trastuzumab Fab (PDB 1N8Z)` as your template

### 2. **Identify Escape Mechanisms**
For each isoform, determine:
- **Δ16HER2**: Does exon-16 deletion disrupt the trastuzumab epitope on domain III?
- **p95HER2**: Is the N-terminal extracellular domain truncated/missing?
- **Point mutants (S310F, L755S, K753E)**: Do they sterically clash with antibody binding or alter the epitope conformation?

### 3. **Map Druggable Surfaces**
Your protocol specifically mentions:
> "Junctional cysteine pocket is exposed; domain-III remains druggable"

Look for:
- Preserved epitopes on resistant isoforms
- Novel surface loops created by splicing junctions
- Accessible pockets for new antibody paratopes

### 4. **QC and Fail/Pass Assessment**
Create your deliverable:
- Contact probability heat-maps (Boltz2)
- pLDDT scores for confidence
- PAE (Predicted Aligned Error) plots
- Flag any models needing re-running with stricter parameters

## Practical Next Actions

1. **Download trastuzumab Fab structure** (PDB: 1N8Z)
2. **Run Boltz2 docking** for each isoform × trastuzumab pair
3. **Visualize in PyMOL/ChimeraX** - Compare WT vs. mutant binding interfaces
4. **Document escape patterns** - Which isoforms lose binding? Where?
5. **Identify candidate epitopes** for your future antibody design (Week 5+)

Would you like help setting up the Boltz2 docking workflow or analyzing the binding interfaces you've predicted?
