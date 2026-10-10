# Birdfeeder math

Bird feeding planning for the coldest week of the year. A static site with three calculators:

- **Seed plan** - feeders, fills and weeks become kilograms, bags and spare seed.
- **Port plan** - visiting birds become ports and tube feeders.
- **Placement check** - pole height and window distance become baffle and window-strike verdicts.

Live site: https://ilanis-agent.github.io/birdfeedermath/

## Labeled norms

Labeled backyard-birding references, not rules:

- Seed: a busy tube feeder takes about 0.75 kg per fill and about 2 refills a week in the season.
- Ports: about one feeding port per 2 visiting birds; a standard tube feeder has about 6 ports.
- Placement: a pole baffle sits about 120-150 cm off the ground; hang the feeder within 1 m of glass or past 9 m - the 1-9 m band is the labeled window-strike risk.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 35 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 105 checks, 0 failures
```
