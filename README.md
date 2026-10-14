# CareNear

A community-reported open/closed status tracker for pharmacies, hospitals, and clinics in Nigeria, with a free map view and "nearest" sorting. No live API reliably tells you whether a specific pharmacy is open right now — so, like the rest of this project series, it's self-reported.

**Not an official directory. In a medical emergency, go to the nearest hospital or call emergency services immediately** rather than relying on this site.

## Features

- **Report a status** — state, area, place name, type (pharmacy/hospital/clinic), open/closed now, optional 24hr flag, optional location pin (click a map or use browser geolocation), optional note. Email required (never shown) to cut spam, rate limited.
- **Find nearby** — browse reports for a state, freshest-and-open sorted first, stale reports (over 6 hours old — status is time-sensitive) visibly flagged and sorted last.
- **Map view** — every pinned place shown on a free Leaflet.js + OpenStreetMap map, color-coded green/red/grey by status and freshness. No API key needed.
- **"Use my location"** — browser geolocation (pure client-side, no backend geocoding service) sorts the list by actual distance from you and centers the map on your position.
- **JSON API** (`/api/places`) — recent reports, optionally filtered by state.

## Why no Google Maps / paid geocoding

Keeping this free to run: OpenStreetMap tiles need no API key, and distance sorting is computed client-side with the haversine formula once you share your location — no geocoding service required at all.

## Tech stack

Flask + Flask-SQLAlchemy, PostgreSQL on Render, server-rendered Jinja2 + Leaflet.js (loaded via CDN, no build step).

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
export $(cat .env | xargs)

python app.py
```

Falls back to local SQLite (`carenear_dev.db`) if `DATABASE_URL` isn't set. Visit `http://localhost:5000`.

## Deploying to Render

**Option A — blueprint:** push to GitHub, "New Blueprint" in Render pointed at the repo — `render.yaml` sets up the web service and free Postgres together.

**Option B — manual:** create a Postgres DB, create a Web Service (`pip install -r requirements.txt` / `gunicorn app:app`), add `DATABASE_URL` and `SECRET_KEY` env vars.

Note: browser geolocation requires HTTPS (Render gives you this automatically) — it won't work over plain HTTP except on `localhost`.

## Project structure

```
app.py              # routes + app factory
models.py           # PlaceReport model
reference_data.py   # states, place types, approximate state-capital centers for map framing
utils.py            # validation, rate limiting, place grouping/sorting
templates/           # index (report form + pin picker), browse (map + list) + shared base layout
static/style.css     # all styling
```

## Known limitations / next steps

- **Place name matching is free text** — same tradeoff as the other projects in this series; "HealthPlus Pharmacy, Allen Ave" and "HealthPlus Allen" are treated as different entries.
- **Location pinning is optional** — a report without a pin still shows in the list, just not on the map or in distance sorting.
- **No real opening-hours schedule** — this is "someone reported open/closed at this time," not a maintained schedule. That's intentional (schedules go stale; a recent human report is more trustworthy for "right now").
- **No email verification**, same tradeoff as the rest of the series.

## License

MIT — see [LICENSE](LICENSE).
