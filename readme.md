https://docs.google.com/document/d/1PTOMLRsIBdl5XNer5PmSpld-OnheUxNBB3auJ8sFSp8/edit?tab=t.0#heading=h.z6dcsim9vf3y
Looking at your protocol, you've completed **Week 2-3 (Structural Prediction)** for your HER2 isoforms. Here's what you originally intended and your clear next steps:

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

# Claude literature summary

[link](https://claude.ai/chat/1ee6b45b-53b8-4f37-a5ee-a0aec9f4ae59)

I'll analyze these papers to identify HER2 isoforms and their drug resistance profiles. Let me fetch and review them systematically.Let me search for information about the papers I couldn't access directly:Let me fetch one of the key papers on L755S and K753E mutations:Let me fetch one more paper on S310F mutation:Based on the papers I've reviewed, here's a comprehensive summary of HER2 isoforms/mutations and their drug resistance profiles:

## **HER2 Isoforms/Mutations and Drug Resistance**

### **1. p95HER2 (Truncated HER2)**

**Drug Resistance:**
- **Resistant to trastuzumab**: Only 1 of 9 patients (11.1%) expressing p95HER2 responded to trastuzumab with a partial response, whereas 19 of 37 patients (51.4%) with tumors expressing full-length HER2 achieved either a complete or partial response (P = 0.029)

- **Sensitive to lapatinib**: Cell lines transfected with p95-HER2 and p95-HER2-expressing xenograft models maintain sensitivity to the HER2 kinase inhibitor lapatinib with diminished p95-HER2 phosphorylation, reduced downstream phosphorylation of AKT, and cell growth inhibition

**Resistance Mechanism:**
p95HER2 is an amino terminally truncated receptor that lacks the extracellular domain and cannot bind to trastuzumab but retains kinase activity

---

### **2. d16HER2 (Delta-16 splice variant)**

**Drug Resistance:**
- **In vitro resistance to trastuzumab**: MCF-7 and NIH3T3 cell lines expressing d16HER2 were found to be refractory to trastuzumab in vitro in cell proliferation and invasion bioassays

- **In vivo sensitivity to trastuzumab**: Trastuzumab, administered in vivo to mice xenografted with MCF10A cells that ectopically expressed d16HER2, blocked tumor growth, and transgenic murine mammary cell lines that express the human d16HER2 variant become sensitive to lapatinib

- **Resistance to T-DM1**: d16HER2-expressing mammary tumor cell lines are resistant to the anti-HER2 therapeutic trastuzumab emtansine (T-DM1), whereas control cells that express wtHER2 are highly sensitive to it

- **Resistance to lapatinib but sensitive to dacomitinib**: d16HER2 transgenic females showed intrinsic resistance to lapatinib, but dacomitinib—an irreversible inhibitor of HER1 and HER2—inhibited the formation of autochthonous mammary tumors

**Resistance Mechanism:**
The binding of trastuzumab to d16HER2 might be impeded by d16HER2 homodimers with disulfide bridges formed through unpaired cysteine residues, although the concomitant high expression of wtHER2 on the tumor cell membrane facilitates the binding and therapeutic activity of trastuzumab

---

### **3. L755S Mutation**

**Drug Resistance:**
- **Resistant to lapatinib**: The HER2L755S mutation was identified as a mechanism of acquired resistance to lapatinib-containing HER2-targeted therapy in HER2-amplified breast cancer models

- **Resistant to trastuzumab and trastuzumab+pertuzumab**: The HER2L755S mutation conferred complete resistance to the dual regimen lapatinib plus trastuzumab and also trastuzumab plus pertuzumab

- **Partial resistance to T-DM1**: The HER2L755S mutation conferred partial resistance to the antibody-drug conjugate trastuzumab emtansine (T-DM1)

- **Sensitive to irreversible TKIs (afatinib and neratinib)**: The HER1/2 irreversible inhibitors afatinib and neratinib substantially inhibited both resistant cell growth and the HER2 and downstream AKT/MAPK signaling driven by HER2L755S in vitro and in vivo

**Resistance Mechanism:**
The HER2L755S mutation disrupts the inactive conformation of the kinase domain, which is required for lapatinib binding, leading to HER2 reactivation through hyperphosphorylation and enhanced MAPK and PI3K-mTOR signaling

---

### **4. K753E Mutation**

**Drug Resistance:**
- **Resistant to lapatinib**: Resistance to lapatinib appears with K753E mutation

- **Sensitive to neratinib**: K753E mutation conferred resistance to lapatinib but showed sensitivity to neratinib

**Resistance Mechanism:**
The importance of electrostatic interactions that occur at the ATP binding site close to these residues contributes to lapatinib resistance

---

### **5. S310F Mutation (Extracellular Domain)**

**Drug Resistance:**
- **Resistant to pertuzumab**: S310F mutant did not react to pertuzumab, and pertuzumab did not inhibit the phosphorylation of HER2 in cells expressing both wild-type HER2 and S310F mutant

- **Trastuzumab shows limited effectiveness**: Trastuzumab did not inhibit the activation of the HER2 receptor or cell proliferation in 5637 cells expressing S310F mutant, suggesting that the S310F HER2 mutant did not form homodimers or heterodimers with wild-type HER2

- **Sensitive to cetuximab (EGFR inhibitor) and tyrosine kinase inhibitors**: Both cetuximab and gefitinib inhibited the activation of HER2 and significantly reduced cell growth, and lapatinib inhibited cell proliferation and reduced HER2 phosphorylation

**Resistance Mechanism:**
S310F HER2 mutant can form an active heterodimer with EGFR, which leads to EGFR-mediated phosphorylation of the S310F mutant. The mutation induces structural changes in domain II of HER2, abolishing its reactivity to pertuzumab, but its ability to form EGFR/HER2 dimers remains intact

---

## **Summary Table**

| **Isoform/Mutation** | **Resistant To** | **Sensitive To** | **Key Mechanism** |
|---------------------|------------------|------------------|-------------------|
| **p95HER2** | Trastuzumab | Lapatinib | Lacks extracellular domain for trastuzumab binding |
| **d16HER2** | Trastuzumab (in vitro), T-DM1, Lapatinib | Trastuzumab (in vivo), Dacomitinib | Homodimers with disulfide bridges block trastuzumab; poor T-DM1 internalization |
| **L755S** | Lapatinib, Trastuzumab, Pertuzumab, partial T-DM1 resistance | Afatinib, Neratinib | Disrupts inactive kinase conformation needed for lapatinib binding |
| **K753E** | Lapatinib | Neratinib | Electrostatic changes at ATP binding site |
| **S310F** | Pertuzumab, Trastuzumab (limited) | Cetuximab, TKIs (lapatinib, gefitinib) | Forms active heterodimers with EGFR; structural changes block pertuzumab binding |
