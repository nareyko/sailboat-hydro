# sailboat-hydro

Zero-Network Python library for FairHelm sailboat hydrodynamic ratios and the
Open European & Nordic Sailboat Benchmark (**93** models).

| Link | URL |
|---|---|
| Methodology | [fairhelm.com/en/yachts/formulas/](https://fairhelm.com/en/yachts/formulas/) |
| Zenodo DOI | [10.5281/zenodo.23374417](https://doi.org/10.5281/zenodo.23374417) |
| PyPI (when published) | `pip install sailboat-hydro` |
| OpenAPI snapshot | [open-data yacht-specs](https://fairhelm.com/open-data/yacht-specs/v1/openapi.yaml) |

## Pages

- [93-model index](models.md) — every card links to its canonical FairHelm URL
- [Formulas](formulas.md) — hull speed, CSF, comfort, D/L, SA/D

## Install (local)

```bash
pip install sailboat-hydro
```

```python
from sailboat_hydro import hull_speed_kn, load_nordic_benchmark

bench = load_nordic_benchmark()
assert bench.model_count == 93
```
