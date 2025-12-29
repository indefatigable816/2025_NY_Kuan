import requests
import json  # Import json module to handle JSON data

ensembl_transcript_id = "ENST00000269571"
url = f"https://rest.ensembl.org/lookup/id/{ensembl_transcript_id}?expand=1"
headers = {"Content-Type": "application/json"}
response = requests.get(url, headers=headers)
data = response.json()

exons = data.get("Exon", [])
cds_start = data["Translation"]["start"]
cds_end = data["Translation"]["end"]
strand = data["strand"]

# Collect CDS exons (those overlapping CDS)
cds_exons = []
for exon in exons:
    # Exon is within CDS if it overlaps CDS region
    exon_start, exon_end = exon["start"], exon["end"]
    overlap_start = max(exon_start, cds_start)
    overlap_end = min(exon_end, cds_end)
    if overlap_start <= overlap_end:
        cds_exons.append({
            "exon": exon,
            "cds_start": overlap_start,
            "cds_end": overlap_end
        })

# Remove sorting by 'exon_number' since it does not exist in the API response
# cds_exons = sorted(cds_exons, key=lambda e: e["exon"]["exon_number"])
# Use the order as provided by the API

# Find exon 16 in the list
exon16 = exons[15]  # 0-based index
exon16_start = exon16["start"]
exon16_end = exon16["end"]

# Calculate CDS base offset for exon 16 start and end
cds_bases_before = 0
exon16_cds_start = None
exon16_cds_end = None

for e in cds_exons:
    e_start = e["cds_start"]
    e_end = e["cds_end"]
    length = e_end - e_start + 1
    if exon16_start == e["exon"]["start"]:
        # Exon 16 start in CDS
        exon16_cds_start = cds_bases_before + 1
    if exon16_end == e["exon"]["end"]:
        # Exon 16 end in CDS
        exon16_cds_end = cds_bases_before + length
    cds_bases_before += length

# Convert CDS base positions to protein positions
if exon16_cds_start and exon16_cds_end:
    prot_start = ((exon16_cds_start - 1) // 3) + 1
    prot_end = ((exon16_cds_end - 1) // 3) + 1
    print(f"Exon 16 starts at amino acid position: {prot_start}")
    print(f"Exon 16 ends at amino acid position: {prot_end}")
    # Print protein sequence of exon 16
    # Fetch the full protein sequence from Ensembl
    prot_url = f"https://rest.ensembl.org/sequence/id/{ensembl_transcript_id}?type=protein"
    prot_response = requests.get(prot_url, headers={"Content-Type": "text/plain"})
    if prot_response.ok:
        protein_seq = prot_response.text.strip().split("\n", 1)[-1].replace("\n", "")
        exon16_prot_seq = protein_seq[prot_start-1:prot_end]
        print(f"Exon 16 protein sequence:\n{exon16_prot_seq}")

        # Create spliced protein sequence (without exon 16 region)
        spliced_protein_seq = protein_seq[:prot_start-1] + protein_seq[prot_end:]
        fasta_header = ">d16HER2"
        with open("d16HER2.fasta", "w") as f:
            f.write(f"{fasta_header}\n")
            for i in range(0, len(spliced_protein_seq), 60):
                f.write(spliced_protein_seq[i:i+60] + "\n")
        print("Spliced protein sequence (without exon 16) saved to d16HER2.fasta")

        # --- PTM info for spliced region (exon 16) ---
        # Load PTM data from proteomics PTM file
        try:
            with open("P04626_proteomics_ptm.json") as ptm_f:
                ptm_data = json.load(ptm_f)
            ptm_found = False
            for feature in ptm_data.get("features", []):
                for ptm in feature.get("ptms", []):
                    peptide_begin = int(feature["begin"])
                    ptm_pos = peptide_begin - 1 + int(ptm["position"])
                    # Check if PTM is within the spliced region
                    if prot_start <= ptm_pos+1 <= prot_end:
                        ptm_found = True
                        print(f"PTM in spliced region (exon 16):")
                        print(f"  PTM: {ptm.get('name')} at protein position {ptm_pos+1}")
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
            if not ptm_found:
                print("No PTM found in the spliced (exon 16) region.")
        except Exception as e:
            print(f"Could not load or parse PTM data: {e}")
    else:
        print("Could not fetch protein sequence from Ensembl.")
else:
    print("Could not map exon 16 to CDS/protein sequence.")