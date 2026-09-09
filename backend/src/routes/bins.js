import { Router } from "express";

export const binsRouter = Router();

// TODO: replace with real Firestore reads once backend/CLAUDE.md's data model is wired up.
// This mock lets the dashboard team build against a stable shape before Firebase is live —
// see CLAUDE.md build sequence step 2/3.
const MOCK_BINS = [
  {
    id: "bin-001",
    location: "Central Park - Gate 2",
    fillPercent: 62,
    status: "ok",
    biodegradable: true,
    nonBiodegradable: true,
  },
  {
    id: "bin-002",
    location: "Main Library - West Entrance",
    fillPercent: 88,
    status: "alert",
    biodegradable: true,
    nonBiodegradable: true,
  },
  {
    id: "bin-003",
    location: "Community Center",
    fillPercent: 34,
    status: "ok",
    biodegradable: true,
    nonBiodegradable: false,
  },
];

binsRouter.get("/", (req, res) => {
  res.json({ bins: MOCK_BINS });
});

binsRouter.get("/:id", (req, res) => {
  const bin = MOCK_BINS.find((b) => b.id === req.params.id);
  if (!bin) return res.status(404).json({ error: "bin not found" });
  res.json(bin);
});

// TODO: POST /:id/telemetry - firmware pushes fill level + sensor readings here
// TODO: POST /:id/classify - firmware pushes an image here, gets back a classification
