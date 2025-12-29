import requests
import json

uniprot_id = "P04626"
url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
response = requests.get(url)

if not response.ok:
    print("Failed to fetch UniProt entry.")
    exit()

data = response.json()

ensembl_proteins = []
ensembl_transcripts = []
ensembl_genes = []

crossrefs = data.get("uniProtKBCrossReferences", [])
for xref in crossrefs:
    if xref.get("database") == "Ensembl":
        ensembl_transcripts.append(xref.get("id"))
        for prop in xref.get("properties", []):
            if prop["key"] == "ProteinId":
                ensembl_proteins.append(prop["value"])
            if prop["key"] == "GeneId":
                ensembl_genes.append(prop["value"])

print("Ensembl transcript IDs:", ensembl_transcripts)
print("Ensembl protein IDs:", ensembl_proteins)
print("Ensembl gene IDs:", ensembl_genes)

# Download transcript FASTA for ENST00000269571.10
transcript_id = "ENST00000269571"
transcript_url = f"https://rest.ensembl.org/sequence/id/{transcript_id}?type=cdna"
transcript_headers = {"Content-Type": "text/x-fasta"}
transcript_response = requests.get(transcript_url, headers=transcript_headers)
if transcript_response.ok:
    with open(f"{transcript_id}.fasta", "w") as f:
        f.write(transcript_response.text)
    print(f"Transcript FASTA saved: {transcript_id}.fasta")
else:
    print(f"Failed to fetch transcript FASTA for {transcript_id}")

# Download protein FASTA for P04626-1 and P04626-2
for protein_id in ["P04626-1", "P04626-2"]:
    protein_url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.fasta"
    protein_response = requests.get(protein_url)
    if protein_response.ok:
        with open(f"{protein_id}.fasta", "w") as f:
            f.write(protein_response.text)
        print(f"Protein FASTA saved: {protein_id}.fasta")
    else:
        print(f"Failed to fetch protein FASTA for {protein_id}")


# Fetch proteomics PTM data from EBI Proteins API
proteomics_ptm_url = f"https://www.ebi.ac.uk/proteins/api/proteomics/ptm/{uniprot_id}"
proteomics_response = requests.get(proteomics_ptm_url, headers={"Accept": "application/json"})
if proteomics_response.ok:
    proteomics_ptm_data = proteomics_response.json()
    with open(f"{uniprot_id}_proteomics_ptm.json", "w") as f:
        json.dump(proteomics_ptm_data, f, indent=2)
    print(f"Proteomics PTM data saved: {uniprot_id}_proteomics_ptm.json")
    print(f"Number of proteomics PTM features: {len(proteomics_ptm_data.get('features', []))}")
else:
    print(f"Failed to fetch proteomics PTM data for {uniprot_id}")

# Create a PTM data file for P04626-2 (starting from amino acid 611)
try:
    with open(f"{uniprot_id}_proteomics_ptm.json") as f:
        ptm_data = json.load(f)
    filtered_features = []
    for feature in ptm_data.get("features", []):
        # For features with 'begin' (1-based), keep only those starting at or after 611
        begin = feature.get("begin")
        if begin is not None and int(begin) >= 611:
            filtered_features.append(feature)
    ptm_data_611 = dict(ptm_data)
    ptm_data_611["features"] = filtered_features
    with open(f"P04626-2_proteomics_ptm.json", "w") as f:
        json.dump(ptm_data_611, f, indent=2)
    print("Filtered PTM data for P04626-2 saved to P04626-2_proteomics_ptm.json")
except Exception as e:
    print(f"Could not create filtered PTM data for P04626-2: {e}")