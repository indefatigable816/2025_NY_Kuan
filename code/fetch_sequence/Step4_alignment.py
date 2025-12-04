import requests
import time

# List of FASTA files to align
fasta_files = [
    "WT_P04626-1.fasta",
    "IS1_p95_P04626-2.fasta",
    "IS2_d16.fasta",
    "IS3_K753E.fasta",
    "IS4_L755S.fasta",
    "IS5_S310F.fasta"
]

# Combine all sequences into a single FASTA string
fasta_str = ""
for fname in fasta_files:
    with open(fname) as f:
        fasta_str += f.read().strip() + "\n"

# Submit job to EBI Clustal Omega REST API
submit_url = "https://www.ebi.ac.uk/Tools/services/rest/clustalo/run"
params = {
    'sequence': fasta_str,
    'stype': 'protein',
    'email': 'indefatigable.md13@nycu.edu.tw'  # Replace with your email if required
}
response = requests.post(submit_url, data=params)
if response.status_code != 200:
    print(f"Failed to submit alignment job: {response.text}")
    exit()
job_id = response.text.strip()
print(f"Submitted Clustal Omega job. Job ID: {job_id}")

# Poll for job status
status_url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{job_id}"
result_url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{job_id}/aln-clustal_num"  # ✅ corrected
while True:
    status = requests.get(status_url).text.strip()
    print(f"Job status: {status}")
    if status == "FINISHED":
        break
    elif status in ("ERROR", "FAILURE"):
        print("Alignment job failed.")
        exit()
    time.sleep(5)

# Download the alignment result
result = requests.get(result_url)
if result.status_code == 200:
    with open("WT_vs_isoform.aln", "w") as f:
        f.write(result.text)
    print("Alignment complete. Results saved to WT_vs_isoform.aln")
else:
    print(f"Failed to retrieve alignment result: {result.text}")

