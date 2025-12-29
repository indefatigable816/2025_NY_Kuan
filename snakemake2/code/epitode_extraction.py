import json

# === Input your AlphaFold 3 JSON file ===
json_path = "fold_wttras0721_1_full_data_0.json"

with open(json_path, 'r') as f:
    data = json.load(f)

# === Edit this based on your chain IDs ===
chain_id = "A"  # ERBB2
contact_chains = ["B", "C"]  # Antibody: light + heavy

# AF3 JSON might contain these keys: 'residueIndex', 'chainIndex', 'plddt', etc.
# You may need to inspect keys if your JSON is differently structured
# For AF3 output via DeepMind or OpenFold-style: adjust accordingly

# Try extracting interface based on inter-chain proximity (if available)

# Inspect the structure of 'pae' to avoid TypeError
try:
    pae = data["pae"]
    print("Type of data['pae']:", type(pae))
    if isinstance(pae, list):
        print("Sample of data['pae'] (first 2 items):", pae[:2])
    else:
        print("data['pae'] keys:", pae.keys())
    # You can now decide how to extract residue indices based on this structure
    chain_indices = data.get("token_chain_ids", None)
    print("chain_indices:", chain_indices)
except KeyError:
    print("Need example JSON structure to proceed — key format not standard.")
except Exception as e:
    print("Error inspecting 'pae':", e)

# Print to inspect available keys
print("Top-level JSON keys:", data.keys())
