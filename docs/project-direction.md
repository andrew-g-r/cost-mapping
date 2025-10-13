# Project direction

## Repository consolidation

`cost-mapping` is the active implementation. The related `cost-topology` repository is an earlier design notebook for the same cost-surface idea: it contains only a README and an image index. This repository adds request and rendering scripts plus a 16×16 sample dataset. Future implementation belongs here. No files or history from the private notebook need to be published or deleted.

## Product question

Help a driver answer: "What does this trip cost, and does the payout cover the trip and my time?"

Keep distance, driving time, work/wait time, vehicle cost, tolls, parking, and desired hourly earnings visible. Offer offline estimates first, with explicit assumptions and optional live routing. Separate cash expenses from the value of time so users do not confuse take-home earnings with the target rate.

## Delivery goals

- Reusable, validated Python models and reproducible sample datasets.
- CLI workflows for single gigs, comparisons, route collection, exports, and cost surfaces.
- A local browser calculator with transparent assumptions and no account or API key requirement.
- Optional plotting and live routing; no mandatory scientific stack for everyday calculations.
- Tests for arithmetic, units, data orientation, interpolation, provider failures, and full workflows.
