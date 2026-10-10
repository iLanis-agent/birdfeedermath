// Birdfeeder math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled backyard-birding norm, not a rule.
(function (root) {
"use strict";

// Labeled norms (common backyard-birding references):
// - Seed: a busy tube feeder takes about 0.75 kg per fill and about 2 refills a week in the season.
// - Ports: about one feeding port per 2 visiting birds; a standard tube feeder has about 6 ports.
// - Placement: a pole baffle sits about 120-150 cm off the ground; feeders hang either within 1 m
//   of glass or past 9 m - the 1-9 m band is the labeled window-strike risk.

function r1(x) { return Math.round(x * 10) / 10; }
function r2(x) { return Math.round(x * 100) / 100; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function seedPlan(feeders, kgPerFill, refillsWeek, weeks, bagKg) {
  if (!positive(feeders, kgPerFill, refillsWeek, weeks, bagKg)) return { error: "all seed inputs must be positive" };
  var totalKg = r1(feeders * kgPerFill * refillsWeek * weeks);
  var bags = Math.ceil(totalKg / bagKg);
  var spareKg = r1(bags * bagKg - totalKg);
  return { feeders: feeders, kgPerFill: r2(kgPerFill), refillsWeek: r1(refillsWeek), weeks: weeks,
    bagKg: r1(bagKg), totalKg: totalKg, bags: bags, spareKg: spareKg };
}

function renderSeed(r) {
  if (r.error) return r.error;
  return r.feeders + " feeder" + (r.feeders === 1 ? "" : "s") + " at a labeled " + r.kgPerFill + " kg per fill, " +
    r.refillsWeek + (r.refillsWeek === 1 ? " fill" : " fills") + " a week for " + r.weeks + " week" + (r.weeks === 1 ? "" : "s") + " is " + r.totalKg +
    " kg of seed - " + r.bags + " bag" + (r.bags === 1 ? "" : "s") + " of " + r.bagKg + " kg, " + r.spareKg + " kg spare.";
}

function portPlan(birds) {
  if (!positive(birds)) return { error: "bird count must be positive" };
  var ports = Math.ceil(birds / 2);
  var feeders = Math.ceil(ports / 6);
  return { birds: birds, ports: ports, feeders: feeders };
}

function renderPorts(r) {
  if (r.error) return r.error;
  return r.birds + " visiting bird" + (r.birds === 1 ? "" : "s") + " want" + (r.birds === 1 ? "s" : "") + " about " + r.ports + " port" + (r.ports === 1 ? "" : "s") + " (labeled one per 2 birds) - " +
    r.feeders + " tube feeder" + (r.feeders === 1 ? "" : "s") + " at a labeled 6 ports each.";
}

function placePlan(poleCm, windowM) {
  if (!positive(poleCm)) return { error: "pole height must be positive" };
  if (typeof windowM !== "number" || !isFinite(windowM) || windowM < 0) return { error: "window distance must be zero or more" };
  var baffle;
  if (poleCm < 120) {
    baffle = "pole is under the labeled 120 cm baffle line - squirrels will climb it";
  } else if (poleCm <= 150) {
    baffle = "mount the baffle at the top of the pole (labeled 120-150 cm)";
  } else {
    baffle = "mount the baffle anywhere in the labeled 120-150 cm band";
  }
  var strike;
  if (windowM < 1 || windowM > 9) {
    strike = "in the labeled strike-safe zone (under 1 m or over 9 m from glass)";
  } else {
    strike = "inside the labeled 1-9 m window-strike band - move it closer to the glass or past 9 m";
  }
  return { poleCm: r1(poleCm), windowM: r1(windowM), baffle: baffle, strike: strike };
}

function renderPlace(r) {
  if (r.error) return r.error;
  return "A " + r.poleCm + " cm pole: " + r.baffle + ". At " + r.windowM + " m from the window the feeder is " + r.strike + ".";
}

var api = {
  seedPlan: seedPlan,
  portPlan: portPlan,
  placePlan: placePlan,
  renderSeed: renderSeed,
  renderPorts: renderPorts,
  renderPlace: renderPlace
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.BirdfeederMath = api;
})(typeof window !== "undefined" ? window : globalThis);
