import "dotenv/config";
import express from "express";
import cors from "cors";

import { binsRouter } from "./routes/bins.js";
import { alertsRouter } from "./routes/alerts.js";
import { store } from "./store/index.js";
import { alertThreshold } from "./services/alerts.js";

const app = express();
app.use(cors());
app.use(express.json({ limit: "5mb" })); // images from ESP-CAM need headroom

app.use("/api/bins", binsRouter);
app.use("/api/alerts", alertsRouter);

app.get("/health", (req, res) =>
  res.json({
    status: "ok",
    store: store.name,
    alertThreshold: alertThreshold(),
  })
);

// Malformed JSON from a firmware POST shouldn't take the process down, and neither should a
// Firestore call failing — return JSON either way so the ESP32's HTTPClient can parse it.
app.use((err, req, res, next) => {
  if (res.headersSent) return next(err);

  const status = err.status && err.status < 500 ? err.status : 500;
  if (status >= 500) console.error("[error]", err);

  res.status(status).json({ error: err.message ?? "internal server error" });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`InnovaMesh backend listening on port ${port}`);
});
