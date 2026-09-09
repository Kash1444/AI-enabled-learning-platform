import { Router } from "express";

import { store } from "../store/index.js";

export const alertsRouter = Router();

const wrap = (handler) => (req, res, next) => handler(req, res, next).catch(next);

/*
 * GET /api/alerts?resolved=false
 * Alerts are raised by the telemetry endpoint — see services/alerts.js.
 */
alertsRouter.get(
  "/",
  wrap(async (req, res) => {
    const { resolved } = req.query;

    const filter =
      resolved === undefined ? {} : { resolved: resolved === "true" };

    res.json({ alerts: await store.listAlerts(filter) });
  })
);

/*
 * POST /api/alerts/:id/resolve — manual acknowledgement from the dashboard.
 * Alerts also clear on their own once a bin's fill level drops back below the threshold.
 */
alertsRouter.post(
  "/:id/resolve",
  wrap(async (req, res) => {
    const alert = await store.resolveAlert(req.params.id);
    if (!alert) return res.status(404).json({ error: "alert not found" });

    res.json(alert);
  })
);
