# Snapshot sync contract

Bundled `nordic_benchmark.json` is derived from FairHelm `mcp-yacht-specs` snapshot.

**SSOT for model JSON:** `fairhelm-2026/packages/mcp-yacht-specs/data/yacht-specs-snapshot.json`  
**Consumer:** `scripts/sync_benchmark.py` → `src/sailboat_hydro/data/nordic_benchmark.json`

## From this sibling checkout

```bash
export FAIRHELM_ROOT=~/projects/fairhelm-2026
python scripts/sync_benchmark.py
# or:
export SAILBOAT_HYDRO_SNAPSHOT=$FAIRHELM_ROOT/packages/mcp-yacht-specs/data/yacht-specs-snapshot.json
python scripts/sync_benchmark.py
```

Default fallback (no env): `~/projects/fairhelm-2026/packages/mcp-yacht-specs/data/yacht-specs-snapshot.json`.

## From FairHelm monorepo (`packages/sailboat-hydro`)

```bash
python packages/sailboat-hydro/scripts/sync_benchmark.py
```

Resolves the sibling `packages/mcp-yacht-specs` path automatically.

## Do not

- Hand-edit `nordic_benchmark.json` without re-running sync from the mcp snapshot.
- Point Repository / Issues at the FairHelm monorepo tree — use `nareyko/sailboat-hydro`.
