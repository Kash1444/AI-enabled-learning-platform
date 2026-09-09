# dashboard/ — context for Claude Code

Plain HTML/CSS/JS monitoring dashboard (no framework — matches the onboarding doc's stack choice).

## What it shows (from the pitch deck mockup)

- Overall bin level across all monitored bins (big % readout)
- A card per bin: location, fill %, biodegradable/non-biodegradable status, alert state
- Alerts when a bin crosses the fill threshold

## Data source

During early development, point `js/app.js` at the backend's mock endpoint:
`GET http://localhost:3000/api/bins` (see `backend/src/routes/bins.js`).
Once Firebase is live, switch to either the Firestore client SDK for realtime updates, or keep
polling the backend — whichever the team decides in the build-sequence step 5 wiring.

## Conventions

- No build step — plain HTML/CSS/JS, opened directly or served statically
- Prettier formatting
- Branch: `feat/dashboard-[description]`
