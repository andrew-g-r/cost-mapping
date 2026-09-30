# Cost Mapping

**Is the trip worth taking?** Calculate trip expenses, net earnings, effective hourly pay, and the payout needed to meet your target. Compare several gigs or explore a geographic cost surface.

Python 3.11+. No runtime dependencies for the CLI, calculator, interpolation, or offline routing. Plotting is optional.

```sh
python3 -m pip install .
cost-mapping serve
```

Open **http://127.0.0.1:8766**. The local calculator shows the full cost breakdown, compares trips, explores ±20% driving-time and operating-cost scenarios, and exports reports. It makes no external network requests. Vehicle cost and hourly target defaults are examples, not official rates.

## Evaluate and compare gigs

```sh
cost-mapping evaluate --payout 30 --miles 10 --driving-minutes 25   --work-minutes 10 --waiting-minutes 5 --tolls 2 --parking 1   --cost-per-mile 0.35 --target-hourly 20
cost-mapping compare examples/gigs.csv --sort effective_hourly
cost-mapping scenarios --payout 30 --miles 10 --driving-minutes 25
```

Enter **all travel, including any return or repositioning miles/minutes**. Vehicle cost should include the operating expenses you want to account for (for example, fuel and wear). Toll and parking expenses are additional. Taxes and costs you do not enter are not included.

- Cash cost = miles × operating cost per mile + tolls + parking.
- Net earnings = payout − cash cost.
- Effective hourly earnings = net earnings ÷ total driving, work, and waiting hours.
- Minimum target payout = cash cost + total hours × target hourly earnings.

The target's time value is shown separately; it is not subtracted twice. Monetary inputs use one consistent currency; the browser labels USD. Calculation results retain precision and the browser rounds only for display.

## Route estimates

```sh
cost-mapping route --origin 30.30,-97.75 --destination 30.35,-97.70 --round-trip
cost-mapping route --origin 30.30,-97.75 --destination 30.35,-97.70   --provider google --round-trip --dry-run
```

Offline routing uses great-circle distance × a road factor (default 1.3), with a stated average speed (25 mph). **It does not know roads, rivers, closures, tolls, or traffic.** Change these assumptions with `--road-factor` and `--speed-mph`.

Live routing requires `--provider google` and `GOOGLE_MAPS_API_KEY` in your environment. It uses the [Google Routes API v2](https://developers.google.com/maps/documentation/routes/compute_route_directions), with a minimal distance/duration field mask. Enable that API and billing in your own Google Cloud project. `--dry-run` shows request counts without sending requests; `--max-requests` bounds them. Round trips request both directions separately. There are no automatic retries or silent offline fallbacks. Provider costs and terms apply. Google responses are not persisted in the synthetic-route cache.

## Cost surfaces

```sh
cost-mapping collect --origin 30.30,-97.75 --bounds 30.2 -97.9 30.4 -97.6   --rows 16 --columns 16 --metric minutes --round-trip --output area.json
cost-mapping query area.json --point 30.31,-97.74
cost-mapping resample area.json --rows 48 --columns 48 --output smooth.json
cost-mapping inspect area.json
cost-mapping reach area.json --budget 20
cost-mapping export area.json --format geojson --output points.geojson
cost-mapping export area.json --format csv --output points.csv
```

`collect` is offline only, so a grid cannot accidentally create hundreds of paid requests. Optional `--cache estimates.sqlite3` reuses synthetic measurements. Grids have latitude rows and longitude columns, include all bounds, and are capped at 100,000 samples. Bilinear interpolation refuses out-of-bounds points. More interpolation points do not create more accurate observations. `reach` reports sampled points within a budget in the dataset's units; it does not invent an isochrone polygon.

## Sample data and plots

```sh
cost-mapping sample --output legacy.json
python3 -m pip install '.[plot]'
cost-mapping plot legacy.json --output heatmap.png
cost-mapping plot legacy.json --kind surface --output surface.png
```

The packaged Austin data comes from the original 2021 array. It has been transposed into the documented axis order and preserves the original exclusive upper bounds. **Its collection accuracy and trip direction are unverified**; use it as a historical demonstration, not a current travel estimate. The original `Z_array.json` remains available.

Plotting uses Matplotlib 3.11.2+; PNG, SVG and PDF output are supported. The removed SciPy `interp2d` API and the Google Maps Python client are no longer runtime dependencies. The old script filenames now delegate to explicit CLI commands and do nothing when imported.

## Files, development, and project scope

All report commands support `--output` and `--force`; existing files are protected by default. See `examples/gigs.csv` for the CSV input schema. JSON surfaces declare their schema version, units, source, and bounds.

```sh
python3 -m pip install -r requirements-dev.txt
ruff check .
ruff format --check .
python3 -m unittest discover -s tests -v
python3 -m pip wheel --no-deps . -w dist
```

`cost-mapping` is the active project. `cost-topology` is the earlier notebook for the same idea and is not used for future implementation. See [project direction](docs/project-direction.md) and [credential guidance](SECURITY.md).

Author: Andrew Russell.
