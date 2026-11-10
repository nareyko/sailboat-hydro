# Publish `sailboat-hydro` to PyPI

Name on PyPI: **`sailboat-hydro`** (verified free as of 2026-10-15).  
Author / maintainer scope: **nareyko** (same as `@nareyko/mcp-yacht-specs`).

## Prerequisites

1. PyPI account with permission to upload `sailboat-hydro`.
2. API token (scope project or account). Prefer Trusted Publisher (GitHub Actions) later; for a one-shot upload use a token.

Store the token outside git, e.g. `backend/.secrets/pypi-token` (gitignored) or `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

TestPyPI (optional dry run):

```ini
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...
```

## Build & verify locally (no token needed)

```bash
# sibling: ~/projects/sailboat-hydro  (or FairHelm packages/sailboat-hydro)
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest -q
export FAIRHELM_ROOT=~/projects/fairhelm-2026   # when not in monorepo
python scripts/sync_benchmark.py
python -m build
python -m twine check dist/*
```

Smoke-install the wheel from a clean venv:

```bash
python -m venv /tmp/sailboat-hydro-smoke
/tmp/sailboat-hydro-smoke/bin/pip install dist/sailboat_hydro-*.whl
/tmp/sailboat-hydro-smoke/bin/python -c "
from sailboat_hydro import hull_speed_kn, load_nordic_benchmark
assert abs(hull_speed_kn(9.35) - 7.43) < 0.01
assert len(load_nordic_benchmark().models) == 93
print('smoke ok', load_nordic_benchmark().zenodo_doi)
"
```

## Upload

TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sailboat-hydro
```

Production PyPI:

```bash
python -m twine upload dist/*
pip install sailboat-hydro==1.0.0
```

## After publish

1. Confirm https://pypi.org/project/sailboat-hydro/
2. Confirm https://github.com/nareyko/sailboat-hydro matches the released tag.
3. Live for-ai / llms lines appear after the next FairHelm frontend deploy.
