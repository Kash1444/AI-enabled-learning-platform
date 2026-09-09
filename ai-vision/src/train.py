"""
Trains the waste classifier: Biodegradable / Non-Biodegradable / Hazardous.

Starting point: transfer learning off MobileNetV2 (small, fast to train, good baseline
accuracy without a large dataset). Swap the base model or go custom CNN once you know
your real accuracy needs and dataset size.

Usage:
    python src/train.py --data-dir path/to/labeled/images --epochs 10

Expects data-dir laid out as:
    data-dir/
        biodegradable/
        non_biodegradable/
        hazardous/
"""

import argparse

# TODO: implement once a labeled dataset exists (see CLAUDE.md "Dataset").
# Skeleton below is the intended shape - fill in as the dataset comes together.


def build_model(num_classes: int = 3):
    """Return a compiled Keras model (MobileNetV2 base + classification head)."""
    raise NotImplementedError


def load_dataset(data_dir: str):
    """Return (train_ds, val_ds) from an image directory."""
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--output", default="models/waste_classifier.h5")
    args = parser.parse_args()

    train_ds, val_ds = load_dataset(args.data_dir)
    model = build_model()
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)
    model.save(args.output)
    print(f"Saved model to {args.output}")


if __name__ == "__main__":
    main()
