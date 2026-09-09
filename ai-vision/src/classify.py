"""
Loads the trained model and classifies a single image.

Meant to be called by the backend (backend/CLAUDE.md) - either wrapped in a small Python
microservice the Express app calls over HTTP, or invoked as a subprocess. Pick one approach
once the backend team is ready to wire step 5 of the build sequence.
"""

LABELS = ["biodegradable", "non_biodegradable", "hazardous"]


def load_model(model_path: str = "models/waste_classifier.h5"):
    # TODO: tf.keras.models.load_model(model_path) once a model exists
    raise NotImplementedError


def classify(model, image_path: str) -> dict:
    """Returns {"label": str, "confidence": float}."""
    # TODO: preprocess image to match training input shape, run model.predict()
    raise NotImplementedError


if __name__ == "__main__":
    import sys

    model = load_model()
    result = classify(model, sys.argv[1])
    print(result)
