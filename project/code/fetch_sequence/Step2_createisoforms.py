from Bio import SeqIO
from Bio.Seq import MutableSeq, Seq
import json

# Read the original FASTA file
input_fasta = "P04626-1.fasta"
record = SeqIO.read(input_fasta, "fasta")

# K753E mutation: Lysine (K) to Glutamic acid (E) at position 753 (1-based)
seq_k753e = MutableSeq(str(record.seq))
seq_k753e[752] = "E"  # 0-based index
record_k753e = record[:]
record_k753e.seq = Seq(str(seq_k753e))
record_k753e.id += "_K753E"
record_k753e.description += " K753E isoform"
with open("P04626-1_K753E.fasta", "w") as f:
    SeqIO.write(record_k753e, f, "fasta")

# L755S mutation: Leucine (L) to Serine (S) at position 755 (1-based)
seq_l755s = MutableSeq(str(record.seq))
seq_l755s[754] = "S"  # 0-based index
record_l755s = record[:]
record_l755s.seq = Seq(str(seq_l755s))
record_l755s.id += "_L755S"
record_l755s.description += " L755S isoform"
with open("P04626-1_L755S.fasta", "w") as f:
    SeqIO.write(record_l755s, f, "fasta")

# S310F mutation: Serine (S) to Phenylalanine (F) at position 310 (1-based)
seq_s310f = MutableSeq(str(record.seq))
seq_s310f[309] = "F"  # 0-based index
record_s310f = record[:]
record_s310f.seq = Seq(str(seq_s310f))
record_s310f.id += "_S310F"
record_s310f.description += " S310F isoform"
with open("P04626-1_S310F.fasta", "w") as f:
    SeqIO.write(record_s310f, f, "fasta")

print("Mutant FASTA files generated: P04626-1_K753E.fasta, P04626-1_L755S.fasta, P04626-1_S310F.fasta")

# Check if mutation sites are PTM sites using proteomics PTM data
ptm_sites = set()
with open("P04626_proteomics_ptm.json") as f:
    ptm_data = json.load(f)
for feature in ptm_data.get("features", []):
    for ptm in feature.get("ptms", []):
        peptide_begin = int(feature["begin"])
        ptm_pos = peptide_begin - 1 + int(ptm["position"])
        ptm_sites.add(ptm_pos)

# Check all mutants
for mut_name, pos in [
    ("K753E", 753),
    ("L755S", 755),
    ("S310F", 310)
]:
    found = False
    for feature in ptm_data.get("features", []):
        for ptm in feature.get("ptms", []):
            peptide_begin = int(feature["begin"])
            ptm_pos = peptide_begin - 1 + int(ptm["position"])
            if pos == ptm_pos:
                found = True
                print(f"{mut_name}: Position {pos} is a PTM site.")
                print(f"  PTM: {ptm.get('name')} at peptide position {ptm.get('position')}")
                if feature.get('peptide'):
                    print(f"  Peptide: {feature.get('peptide')}")
                if ptm.get('sources'):
                    print(f"  Source(s): {', '.join(ptm.get('sources'))}")
                if ptm.get('dbReferences'):
                    for ref in ptm.get('dbReferences'):
                        print(f"    Reference: {ref.get('id')} (Dataset: {ref.get('properties', {}).get('Dataset ID', 'N/A')})")
                if feature.get('evidences'):
                    for ev in feature.get('evidences'):
                        print(f"    Evidence: {ev.get('code')} from {ev.get('source', {}).get('id', '')}")
    if not found:
        print(f"{mut_name}: Position {pos} is NOT a PTM site.")