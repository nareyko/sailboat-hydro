# sailboat-hydro

**Zero-Network** Python library for FairHelm sailboat hydrodynamic ratios and the Open European & Nordic Sailboat Benchmark (93 models).

Docs pack (MkDocs / RTD / GH Pages PREP): [`docs/`](./docs/) · [`PUBLISH-DOCS.md`](./PUBLISH-DOCS.md) · regenerate with `python scripts/generate_docs_models.py`.

Formulas and the JSON snapshot ship inside the wheel. Calls run locally. There is **no HTTP** to `api.fairhelm.com`, no Postgres, and no CapEx / listing decoder.

| Link | URL |
|---|---|
| **Methodology (formulas)** | https://fairhelm.com/en/yachts/formulas/ |
| **Docs (93 models)** | https://nareyko.github.io/sailboat-hydro/ |
| **Open data / OpenAPI** | https://fairhelm.com/open-data/yacht-specs/v1/openapi.yaml |
| **Benchmark DOI** | https://doi.org/10.5281/zenodo.23374417 |
| **GitHub** | https://github.com/nareyko/sailboat-hydro |
| **Publisher (Arviser)** | https://arviser.com/ |
| **Sibling MCP (npm)** | https://www.npmjs.com/package/@nareyko/mcp-yacht-specs |
| **Listing review (€49)** | https://fairhelm.com/en/yachts/services/listing-review/ |

## Install

```bash
pip install sailboat-hydro
```

From a local checkout of this monorepo package:

```bash
pip install -e "packages/sailboat-hydro[dev]"
```

## Quick start

```python
from sailboat_hydro import (
    hull_speed_kn,
    capsize_screening,
    displacement_length_ratio,
    comfort_ratio,
    sail_area_displacement,
    load_nordic_benchmark,
)

print(hull_speed_kn(9.35))                 # ~7.43 kn
print(capsize_screening(3.55, 7500))       # ~1.829
print(displacement_length_ratio(7500, 9.35))
print(
    comfort_ratio(
        displacement_kg=7500,
        lwl_m=9.35,
        loa_m=10.87,
        beam_m=3.55,
    )
)

bench = load_nordic_benchmark()            # 93 models, local JSON only
hr36 = bench.get("hallberg-rassy", "hr36")
assert hr36 is not None
print(hr36.name, hr36.hull_speed_kn, hr36.canonical_model_url)
print(bench.zenodo_doi)
```

## API

| Function | Meaning |
|---|---|
| `hull_speed_kn(lwl_m)` | Theoretical hull speed (kn) |
| `capsize_screening(beam_m, displacement_kg)` | CSF |
| `displacement_length_ratio(disp_kg, lwl_m)` | D/L |
| `comfort_ratio(...)` | Brewer comfort ratio |
| `sail_area_displacement(sa_m2, disp_kg)` | SA/D |
| `load_nordic_benchmark()` | Bundled 93-model Nordic/European benchmark |

Formula constants match `@nareyko/mcp-yacht-specs` (`packages/mcp-yacht-specs/src/formulas.ts`) and the FairHelm frontend formula SSOT. Refresh the bundled JSON (see [`SYNC.md`](./SYNC.md)):

```bash
python packages/sailboat-hydro/scripts/sync_benchmark.py
```

Canonical public repo: [nareyko/sailboat-hydro](https://github.com/nareyko/sailboat-hydro) · sibling `~/projects/sailboat-hydro`.
## Citation

Please cite FairHelm formulas and the Zenodo deposit:

```bibtex
@misc{fairhelm_sailboat_benchmark_2026,
  title        = {Open European \& Nordic Sailboat Benchmark (93 Models)},
  author       = {Nareyko, Vadim and FairHelm},
  year         = {2026},
  doi          = {10.5281/zenodo.23374417},
  url          = {https://doi.org/10.5281/zenodo.23374417},
  howpublished = {FairHelm / CERN Zenodo},
  note         = {Methodology: https://fairhelm.com/en/yachts/formulas/}
}
```

Also see [`CITATION.cff`](./CITATION.cff).

## Develop / test

```bash
cd packages/sailboat-hydro
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest -q
```

## Publish (owner)

See [`PUBLISH.md`](./PUBLISH.md). Build artifacts land in `dist/`.

## License

MIT. See [LICENSE](./LICENSE).
