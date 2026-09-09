import { Router } from "express";

import { store } from "../store/index.js";
import { evaluateFillLevel, statusForFillLevel } from "../services/alerts.js";
import { classify, compartmentFor } from "../services/classifier.js";

export const binsRouter = Router();

/** Wraps an async handler so a rejected promise reaches the error middleware. */
const wrap = (handler) => (req, res, next) => handler(req, res, next).catch(next);

/** Loads the bin named in the URL, or 404s. */
const loadBin = wrap(async (req, res, next) => {
  const bin = await store.getBin(req.params.id);
  if (!bin) return res.status(404).json({ error: "bin not found" });

  req.bin = bin;
  next();
});

// ---------------------------------------------------------------------------
// Reads — consumed by the dashboard
// ---------------------------------------------------------------------------

binsRouter.get(
  "/",
  wrap(async (req, res) => {
    res.json({ bins: await store.listBins() });
  })
);

binsRouter.get("/:id", loadBin, (req, res) => {
  res.json(req.bin);
});

binsRouter.get(
  "/:id/events",
  loadBin,
  wrap(async (req, res) => {
    const limit = Number(req.query.limit) || 20;
    res.json({ events: await store.listEvents(req.params.id, limit) });
  })
);

// ---------------------------------------------------------------------------
// Writes — pushed by the firmware
// ---------------------------------------------------------------------------

/*
 * POST /api/bins/:id/telemetry
 *
 * Body: { fillPercent, moisture?, metalDetected? }
 * Called once per deposit cycle after the ultrasonic reading (firmware step 5).
 * Raises or clears the fill-level alert as a side effect.
 */
binsRouter.post(
  "/:id/telemetry",
  loadBin,
  wrap(async (req, res) => {
    const { fillPercent, moisture, metalDetected } = req.body ?? {};

    if (typeof fillPercent !== "number" || !Number.isFinite(fillPercent)) {
      return res.status(400).json({ error: "fillPercent must be a number" });
    }

    if (fillPercent < 0 || fillPercent > 100) {
      return res.status(400).json({ error: "fillPercent must be between 0 and 100" });
    }

    const patch = {
      fillPercent: Math.round(fillPercent),
      status: statusForFillLevel(fillPercent),
    };

    if (typeof moisture === "number") patch.moisture = moisture;
    if (typeof metalDetected === "boolean") patch.metalDetected = metalDetected;

    const bin = await store.updateBin(req.params.id, patch);
    const alert = await evaluateFillLevel(store, bin);

    res.json({ bin, alert });
  })
);

/*
 * POST /api/bins/:id/classify
 *
 * Body: { image?, moisture?, metalDetected? }  — image is a base64 JPEG from the ESP-CAM.
 * Returns the label plus the compartment the diverter servo should route to.
 *
 * The classifier itself is still a stub (see services/classifier.js); this endpoint is the
 * contract the firmware codes against in the meantime.
 */
binsRouter.post(
  "/:id/classify",
  loadBin,
  wrap(async (req, res) => {
    const { image, moisture, metalDetected } = req.body ?? {};

    const result = await classify({ image, moisture, metalDetected });
    const compartment = compartmentFor(result.label);

    await store.addEvent(req.params.id, {
      label: result.label,
      confidence: result.confidence,
      source: result.source,
    });

    res.json({ ...result, compartment });
  })
);
