# CLPS Lunar Mission Browser

NASA Space Apps Challenge 2026 — [CLPS Lunar Mission Browser](https://www.spaceappschallenge.org/2026/challenges/clps-lunar-mission-browser/).

Compare lunar south-pole landing sites at a glance: when the Sun is up (power) and when Earth is up (direct-to-Earth comms).

## Run

```bash
python3 -m http.server 8000
```

Open http://localhost:8000. `data.json` is committed, so no network is needed.

To refresh the data for another window, for example 30 days from 1 March 2027:

```bash
python3 fetch.py 2027-03-01 30
```

Sun and Earth azimuth and elevation come from the [JPL Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html), observed from `coord@301` (the lunar surface, DE441 ephemeris). The code uses only the Python standard library and has no front-end dependencies.

## Known limits / next steps
1. **Terrain horizon.** The horizon is currently a smooth sphere. The slider only fakes site height as horizon dip. The real fix is to compute a horizon mask per azimuth from a LOLA DEM. This is the biggest accuracy gain and should set the project apart.
2. **Site coordinates are approximate.** Replace them with official Artemis III and CLPS candidate coordinates.
3. Date picker in the UI that calls Horizons live, or a backend that proxies it.
4. Sun disk (0.27° radius) instead of Sun center, so partial illumination counts.
5. Azimuth view: a polar plot of the Sun and Earth tracks against the horizon mask.
