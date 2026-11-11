# Snapshot sync contract

Bundled `nordic_benchmark.json` is derived from FairHelm `mcp-yacht-specs` snapshot.

**Canonical GitHub:** https://github.com/nareyko/sailboat-hydro · sibling `~/projects/sailboat-hydro`  
**SSOT for model JSON:** `packages/mcp-yacht-specs/data/yacht-specs-snapshot.json`  
**Consumer:** `scripts/sync_benchmark.py` → `src/sailboat_hydro/data/nordic_benchmark.json`

## From FairHelm monorepo

```bash
python packages/sailboat-hydro/scripts/sync_benchmark.py
```

## From sibling checkout

```bash
export FAIRHELM_ROOT=~/projects/fairhelm-2026
python scripts/sync_benchmark.py
```

See sibling [`SYNC.md`](https://github.com/nareyko/sailboat-hydro/blob/main/SYNC.md) for env details.
