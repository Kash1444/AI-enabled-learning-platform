# VAPT checklist

Run this once the pipeline is stable (build sequence step 7 in root `CLAUDE.md`) — pentesting a
still-changing system just means re-testing everything after every merge.

## IoT ↔ cloud endpoints

- [ ] Firmware-to-backend telemetry endpoint requires auth (device token / API key, not open POST)
- [ ] Image upload endpoint validates content-type and size before passing to the classifier
- [ ] No API keys or Firebase credentials hardcoded in firmware source (check `main.cpp` and any
      committed config before every push — `serviceAccountKey.json` must never leave `backend/`
      and must be gitignored)
- [ ] TLS on all firmware→backend and backend→Firebase traffic
- [ ] Firestore security rules restrict writes to authenticated devices, not `allow read, write: if true`
- [ ] Dashboard doesn't expose Firebase admin credentials client-side (client SDK config is fine,
      admin SDK keys are not)
- [ ] Rate limiting on public-facing endpoints (telemetry, image upload, QR report submission)
- [ ] QR-code reporting flow doesn't allow arbitrary command injection or unvalidated redirects

## Report

Write findings into this folder as `vapt-report.md` once testing is done, following whatever
format your coursework/SIH submission expects.
