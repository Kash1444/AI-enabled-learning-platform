/*
 * Fill-level alerting.
 *
 * Called on every telemetry POST. Raises an alert when a bin crosses the threshold, and clears it
 * again once the bin is emptied — so a truck emptying a bin doesn't leave a stale alert on the
 * dashboard.
 */

const DEFAULT_THRESHOLD = 80;

/** Read at call time rather than module load, so .env ordering can't catch us out. */
export function alertThreshold() {
  const parsed = Number(process.env.ALERT_THRESHOLD);
  return Number.isFinite(parsed) ? parsed : DEFAULT_THRESHOLD;
}

/**
 * Reconciles a bin's alert state with its current fill level.
 * Returns the alert that was raised, or null if nothing changed.
 */
export async function evaluateFillLevel(store, bin) {
  const threshold = alertThreshold();
  const openAlert = await store.findOpenAlert(bin.id);

  if (bin.fillPercent >= threshold) {
    // Already alerting — don't raise a duplicate on every telemetry POST.
    if (openAlert) return null;

    return store.addAlert({
      binId: bin.id,
      location: bin.location,
      threshold,
      fillPercent: bin.fillPercent,
    });
  }

  // Back below the threshold: the bin has been emptied.
  if (openAlert) {
    await store.resolveAlert(openAlert.id);
  }

  return null;
}

/** Bin status the dashboard colour-codes on. */
export function statusForFillLevel(fillPercent) {
  return fillPercent >= alertThreshold() ? "alert" : "ok";
}
