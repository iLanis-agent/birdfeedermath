#!/usr/bin/env python3
"""Independent oracle for Birdfeeder math. Mirrors engine.js float ops exactly."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def seed_plan(feeders, kg_per_fill, refills_week, weeks, bag_kg):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0
               for v in (feeders, kg_per_fill, refills_week, weeks, bag_kg)):
        return {"error": "all seed inputs must be positive"}
    total_kg = r1(feeders * kg_per_fill * refills_week * weeks)
    bags = math.ceil(total_kg / bag_kg)
    spare_kg = r1(bags * bag_kg - total_kg)
    return {"feeders": feeders, "kgPerFill": r2(kg_per_fill), "refillsWeek": r1(refills_week), "weeks": weeks,
            "bagKg": r1(bag_kg), "totalKg": total_kg, "bags": bags, "spareKg": spare_kg}

def render_seed(r):
    if "error" in r: return r["error"]
    fs = "" if r["feeders"] == 1 else "s"
    ws = "" if r["weeks"] == 1 else "s"
    bs = "" if r["bags"] == 1 else "s"
    rw = " fill" if r["refillsWeek"] == 1 else " fills"
    return (f"{r['feeders']} feeder{fs} at a labeled {num(r['kgPerFill'])} kg per fill, {num(r['refillsWeek'])}"
            f"{rw} a week for {r['weeks']} week{ws} is {num(r['totalKg'])} kg of seed - {r['bags']} bag{bs}"
            f" of {num(r['bagKg'])} kg, {num(r['spareKg'])} kg spare.")

def port_plan(birds):
    if not (isinstance(birds, (int, float)) and math.isfinite(birds) and birds > 0):
        return {"error": "bird count must be positive"}
    ports = math.ceil(birds / 2)
    feeders = math.ceil(ports / 6)
    return {"birds": birds, "ports": ports, "feeders": feeders}

def render_ports(r):
    if "error" in r: return r["error"]
    fs = "" if r["feeders"] == 1 else "s"
    bs = "" if r["birds"] == 1 else "s"
    wv = "s" if r["birds"] == 1 else ""
    ps = "" if r["ports"] == 1 else "s"
    return (f"{r['birds']} visiting bird{bs} want{wv} about {r['ports']} port{ps} (labeled one per 2 birds) - "
            f"{r['feeders']} tube feeder{fs} at a labeled 6 ports each.")

def place_plan(pole_cm, window_m):
    if not (isinstance(pole_cm, (int, float)) and math.isfinite(pole_cm) and pole_cm > 0):
        return {"error": "pole height must be positive"}
    if not (isinstance(window_m, (int, float)) and math.isfinite(window_m) and window_m >= 0):
        return {"error": "window distance must be zero or more"}
    if pole_cm < 120:
        baffle = "pole is under the labeled 120 cm baffle line - squirrels will climb it"
    elif pole_cm <= 150:
        baffle = "mount the baffle at the top of the pole (labeled 120-150 cm)"
    else:
        baffle = "mount the baffle anywhere in the labeled 120-150 cm band"
    if window_m < 1 or window_m > 9:
        strike = "in the labeled strike-safe zone (under 1 m or over 9 m from glass)"
    else:
        strike = "inside the labeled 1-9 m window-strike band - move it closer to the glass or past 9 m"
    return {"poleCm": r1(pole_cm), "windowM": r1(window_m), "baffle": baffle, "strike": strike}

def render_place(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['poleCm'])} cm pole: {r['baffle']}. At {num(r['windowM'])} m from the window the feeder is {r['strike']}.")

cases = []
for f, k, rw, w, b in [(2, 0.75, 2, 4, 5), (1, 0.75, 2, 1, 5), (3, 1, 3, 8, 12.75), (1, 0.5, 1, 2, 2),
                       (2, 0.75, 2, 4, 5.5), (4, 1, 2, 12, 20), (0, 0.75, 2, 4, 5), (2, 0, 2, 4, 5),
                       (2, 0.75, 0, 4, 5), (2, 0.75, 2, 0, 5), (2, 0.75, 2, 4, 0), (-1, 0.75, 2, 4, 5)]:
    res = seed_plan(f, k, rw, w, b)
    cases.append({"fn": "seedPlan", "args": [f, k, rw, w, b], "result": res, "render": render_seed(res)})
for n in [10, 1, 2, 12, 13, 24, 25, 0, -5, 7, 3]:
    res = port_plan(n)
    cases.append({"fn": "portPlan", "args": [n], "result": res, "render": render_ports(res)})
for p, m in [(180, 5), (180, 0.5), (180, 10), (140, 3), (100, 5), (120, 9), (150, 1), (200, 12),
             (0, 5), (180, -2), (90, 0), (175, 8.9)]:
    res = place_plan(p, m)
    cases.append({"fn": "placePlan", "args": [p, m], "result": res, "render": render_place(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
