import requests
import json


if __name__ == "__main__":
    sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"  # Replace with your sequence value of interest
    headers = {
    "content-type": "application/json"
    }
    data = {
    "polymers": [
        {
        "id": "A",
        "molecule_type": "protein",
        "sequence": sequence
        }
    ],
    "recycling_steps": 3,
    "sampling_steps": 50,
    "diffusion_samples": 1,
    "step_scale": 1.638,
    "output_format": "mmcif"
    }
    print("Making request...")
    response = requests.post("http://localhost:8000/biology/mit/boltz2/predict", headers=headers, data=json.dumps(data))
    result = response.json()
    print("Structure prediction completed")
    # Access the first predicted structure
    if result.get("structures"):
        structure = result["structures"][0]
        print(f"Structure format: {structure['format']}")
        print(f"Confidence score: {result['confidence_scores'][0]}")