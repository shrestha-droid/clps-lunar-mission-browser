#!/usr/bin/env python3
"""Pull Sun/Earth elevation at lunar sites from JPL Horizons -> data.json.

usage: python3 fetch.py [START YYYY-MM-DD] [DAYS]
"""
import json, sys, time, urllib.parse, urllib.request
from datetime import date, timedelta

# ponytail: approximate coordinates, no terrain/horizon mask. Replace with
# official NASA site coords and a DEM-based horizon when accuracy matters.
SITES = {
    "Shackleton rim":   (0.0, -89.9),
    "Connecting ridge": (222.0, -89.4),
    "Malapert massif":  (0.0, -85.9),
    "Mons Mouton":      (29.2, -84.8),
    "Haworth rim":      (-5.0, -87.4),
    "Nobile rim":       (31.5, -85.4),
}
STEP_H = 3


def parse(text):
    """Return [(utc_label, azimuth, elevation)] from a Horizons CSV block."""
    body = text.split("$$SOE")[1].split("$$EOE")[0]
    rows = []
    for line in body.strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        rows.append((p[0], float(p[-3]), float(p[-2])))
    return rows


def horizons(body_id, lon, lat, start, stop):
    q = {"format": "json", "COMMAND": f"'{body_id}'", "OBJ_DATA": "'NO'",
         "MAKE_EPHEM": "'YES'", "EPHEM_TYPE": "'OBSERVER'",
         "CENTER": "'coord@301'", "COORD_TYPE": "'GEODETIC'",
         "SITE_COORD": f"'{lon},{lat},0'", "START_TIME": f"'{start}'",
         "STOP_TIME": f"'{stop}'", "STEP_SIZE": f"'{STEP_H} h'",
         "QUANTITIES": "'4'", "CSV_FORMAT": "'YES'"}
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q)
    return parse(json.load(urllib.request.urlopen(url, timeout=60))["result"])


if __name__ == "__main__":
    assert parse("x$$SOE\n 2027-Mar-01 00:00, , , 265.5,  -0.6,\n$$EOE") == [("2027-Mar-01 00:00", 265.5, -0.6)]
    start = sys.argv[1] if len(sys.argv) > 1 else "2027-03-01"
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    stop = (date.fromisoformat(start) + timedelta(days=days)).isoformat()
    out = {"start": start, "step_h": STEP_H, "sites": []}
    for name, (lon, lat) in SITES.items():
        sun = horizons(10, lon, lat, start, stop)
        earth = horizons(399, lon, lat, start, stop)
        out["sites"].append({"name": name, "lon": lon, "lat": lat, "t": [r[0] for r in sun],
                             "sun": [r[2] for r in sun], "earth": [r[2] for r in earth]})
        print("fetched", name, flush=True)
        time.sleep(1)
    json.dump(out, open("data.json", "w"), separators=(",", ":"))
