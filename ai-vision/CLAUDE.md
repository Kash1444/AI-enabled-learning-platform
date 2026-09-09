# ai-vision/ — context for Claude Code

TensorFlow model that classifies a waste image into Biodegradable / Non-Biodegradable / Hazardous.

## Where this runs

The ESP32/ESP-CAM cannot run a full TensorFlow model on-device. Default plan: the backend
(`backend/`) calls into this module (or a saved model it loads) to classify images the firmware
uploads. See root `CLAUDE.md` → "Key technical decisions" before changing this.

## Suggested pipeline

1. `src/train.py` — trains a classifier (start with a small CNN or transfer learning off
   MobileNetV2 — cheap enough to train fast, small enough to matter if you ever move to
   TFLite-Micro on-device)
2. Export to `models/` (gitignored — large binary, don't commit)
3. `src/classify.py` — loads the trained model, exposes a `classify(image) -> {label, confidence}`
   function the backend can call (either as a Python microservice or via a Node-compatible export)

## Dataset

Not yet collected. Public waste-classification datasets (TrashNet, Kaggle garbage classification
sets) are reasonable starting points to bootstrap before collecting your own labeled photos from
the physical prototype.

## Conventions

- Python, black formatting
- `requirements.txt` for dependencies, not a notebook-only workflow — this needs to run headless
  from the backend
- Branch: `feat/ai-vision-[description]`
