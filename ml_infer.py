# app/ml_infer.py
import os, json, numpy as np
from io import BytesIO
from PIL import Image
from keras.models import load_model
from keras.applications.efficientnet import preprocess_input

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
MODEL_DIR = os.path.join(BASE_DIR, "cotton_model")
MODEL_PATH = os.path.join(MODEL_DIR, "cotton_model.h5")
LABELS_PATH = os.path.join(MODEL_DIR, "class_names.json")
DATASET_DIR = os.path.join(BASE_DIR, "training", "dataset")  # fallback source for labels
IMG_SIZE = (224, 224)

_MODEL = None
_CLASS_NAMES = None

def _rebuild_labels_from_dataset():
    if not os.path.isdir(DATASET_DIR):
        return None
    classes = sorted([d for d in os.listdir(DATASET_DIR)
                      if os.path.isdir(os.path.join(DATASET_DIR, d))])
    if classes:
        os.makedirs(MODEL_DIR, exist_ok=True)
        with open(LABELS_PATH, "w") as f:
            json.dump(classes, f)
        return classes
    return None

def _load_artifacts():
    global _MODEL, _CLASS_NAMES
    if _MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model file not found: {MODEL_PATH}")
        _MODEL = load_model(MODEL_PATH)

    if _CLASS_NAMES is None:
        if os.path.exists(LABELS_PATH):
            with open(LABELS_PATH, "r") as f:
                _CLASS_NAMES = json.load(f)
        else:
            # try to rebuild from dataset; if still none, synthesize generic labels
            rebuilt = _rebuild_labels_from_dataset()
            if rebuilt:
                _CLASS_NAMES = rebuilt
            else:
                # fall back to generic indices based on model output size
                out_units = _MODEL.outputs[0].shape[-1]
                _CLASS_NAMES = [f"class_{i}" for i in range(int(out_units))]

def get_labels():
    _load_artifacts()
    return _CLASS_NAMES

def _preprocess_pil(pil_img: Image.Image) -> np.ndarray:
    img = pil_img.convert("RGB").resize(IMG_SIZE)
    x = np.asarray(img, dtype="float32")
    x = preprocess_input(x)
    return np.expand_dims(x, axis=0)

def predict_image_bytes(img_bytes: bytes):
    try:
        _load_artifacts()

        pil = Image.open(BytesIO(img_bytes))
        x = _preprocess_pil(pil)

        # --- Run inference ---
        probs = _MODEL.predict(x, verbose=0)[0]

        if probs is None or len(probs) == 0:
            raise ValueError("Model returned empty predictions")

        labels = get_labels()
        n_probs = len(probs)
        n_labels = len(labels)

        # --- Fix label mismatch dynamically ---
        if n_probs != n_labels:
            print(f"[WARN] Model output {n_probs} != labels {n_labels}. Adjusting.")
            if n_probs > n_labels:
                labels += [f"class_{i}" for i in range(n_labels, n_probs)]
            else:
                labels = labels[:n_probs]

        idx = int(np.argmax(probs))
        confidence = float(probs[idx])

        # --- Low-confidence safeguard ---
        if confidence < 0.5:
            return {
                "prediction": "Uncertain / Not a cotton leaf",
                "confidence": confidence,
                "probabilities": {labels[i]: float(p) for i, p in enumerate(probs)},
            }

        return {
            "prediction": labels[idx],
            "confidence": confidence,
            "probabilities": {labels[i]: float(p) for i, p in enumerate(probs)},
        }

    except Exception as e:
        return {
            "prediction": None,
            "confidence": 0.0,
            "error": str(e),
            "detail": "Unreadable or invalid image"
        }

