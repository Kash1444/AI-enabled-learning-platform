/*
 * Classification proxy.
 *
 * PLACEHOLDER. The real implementation calls into ai-vision/ (build-sequence step 4/5) — this
 * exists now so the firmware team has a stable request/response contract to code the diverter
 * servo against before the model is trained. It does NOT look at the image.
 *
 * What it does instead: derives a label from the secondary sensor readings the firmware already
 * sends alongside the image (moisture → biodegradable, metal → non-biodegradable), which is
 * enough to drive an end-to-end demo. Confidence is deliberately capped low so a stubbed result
 * is never mistaken for a real one.
 */

export const WASTE_LABELS = ["biodegradable", "non-biodegradable", "hazardous"];

// Above this, the moisture sensor is reading wet organic waste.
const MOISTURE_WET_THRESHOLD = 55;

/**
 * @param {object} input
 * @param {string} [input.image]          base64 JPEG from the ESP-CAM (ignored by the stub)
 * @param {number} [input.moisture]       0-100
 * @param {boolean} [input.metalDetected] inductive proximity sensor
 * @returns {Promise<{label: string, confidence: number, source: string}>}
 */
export async function classify({ moisture, metalDetected } = {}) {
  let label = "non-biodegradable";

  if (metalDetected) {
    label = "non-biodegradable";
  } else if (typeof moisture === "number" && moisture >= MOISTURE_WET_THRESHOLD) {
    label = "biodegradable";
  }

  return {
    label,
    confidence: 0.5,
    source: "stub",
  };
}

/**
 * Which compartment the diverter servo routes to. Kept next to the classifier so firmware and
 * backend agree on the vocabulary.
 */
export function compartmentFor(label) {
  switch (label) {
    case "biodegradable":
      return "bio";
    case "hazardous":
      return "hazardous";
    default:
      return "non-bio";
  }
}
