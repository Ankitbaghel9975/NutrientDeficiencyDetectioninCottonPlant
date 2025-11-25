import os
from PIL import Image
import imagehash

REFERENCE_DIR = os.path.join(os.path.dirname(__file__), "..", "training", "dataset")
REFERENCE_DIR = os.path.abspath(REFERENCE_DIR)

# Precompute reference image hashes
reference_hashes = []
for cls in os.listdir(REFERENCE_DIR):
    cls_path = os.path.join(REFERENCE_DIR, cls)
    if os.path.isdir(cls_path):
        for img_file in os.listdir(cls_path):
            img_path = os.path.join(cls_path, img_file)
            try:
                img = Image.open(img_path).convert("RGB").resize((224,224))
                h = imagehash.average_hash(img)
                reference_hashes.append({"class": cls, "hash": h, "path": img_path})
            except Exception as e:
                print(f"Error reading {img_path}: {e}")

def predict_disease(img_path: str):
    """Match uploaded image against reference dataset by hash similarity"""
    img = Image.open(img_path).convert("RGB").resize((224,224))
    h = imagehash.average_hash(img)

    best_match = None
    best_dist = 1e9

    for ref in reference_hashes:
        dist = abs(h - ref["hash"])  # Hamming distance
        if dist < best_dist:
            best_dist = dist
            best_match = ref

    if best_match:
        confidence = float(1 - best_dist/64)  # normalize
        return {"prediction": best_match["class"], "confidence": confidence}
    else:
        return {"prediction": "Unknown", "confidence": 0.0}
