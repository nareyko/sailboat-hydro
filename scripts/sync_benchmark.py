#!/usr/bin/env python3
"""Copy hydro benchmark JSON from mcp-yacht-specs snapshot (FairHelm SSOT).

Resolution order for the snapshot file:
  1. SAILBOAT_HYDRO_SNAPSHOT — absolute path to yacht-specs-snapshot.json
  2. FAIRHELM_ROOT — <root>/packages/mcp-yacht-specs/data/yacht-specs-snapshot.json
  3. Monorepo layout — ../../mcp-yacht-specs/... when this package lives under packages/
  4. Sibling default — ~/projects/fairhelm-2026/packages/mcp-yacht-specs/data/...
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parents[1]
DEST = PKG_ROOT / "src/sailboat_hydro/data/nordic_benchmark.json"


def resolve_snapshot() -> Path:
    env_snap = os.environ.get("SAILBOAT_HYDRO_SNAPSHOT")
    if env_snap:
        return Path(env_snap)

    fairhelm = os.environ.get("FAIRHELM_ROOT")
    if fairhelm:
        return (
            Path(fairhelm) / "packages/mcp-yacht-specs/data/yacht-specs-snapshot.json"
        )

    monorepo = PKG_ROOT.parent / "mcp-yacht-specs/data/yacht-specs-snapshot.json"
    if monorepo.is_file():
        return monorepo

    return (
        Path.home()
        / "projects/fairhelm-2026/packages/mcp-yacht-specs/data/yacht-specs-snapshot.json"
    )


def main() -> int:
    src = resolve_snapshot()
    if not src.is_file():
        print(f"missing snapshot: {src}", file=sys.stderr)
        print(
            "Set SAILBOAT_HYDRO_SNAPSHOT or FAIRHELM_ROOT, or keep the FairHelm monorepo layout.",
            file=sys.stderr,
        )
        return 1
    payload = json.loads(src.read_text(encoding="utf-8"))
    out = {
        "schema_version": payload["schema_version"],
        "generated_at": payload["generated_at"],
        "source": payload["source"],
        "zenodo_doi": "https://doi.org/10.5281/zenodo.23374417",
        "formulas_methodology_url": "https://fairhelm.com/en/yachts/formulas/",
        "open_data_url": "https://fairhelm.com/open-data/yacht-specs/v1/openapi.yaml",
        "model_count": payload["model_count"],
        "formulas": payload["formulas"],
        "models": payload["models"],
    }
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"wrote {DEST} ({len(out['models'])} models) from {src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
