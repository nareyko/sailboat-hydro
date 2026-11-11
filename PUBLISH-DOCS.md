# Publish docs: Read the Docs + GitHub Pages (local PREP)

**Do not** import RTD or `gh-deploy` from CI/agent. Generate + build locally only.

## Generate pages (agent/local)

```bash
cd packages/sailboat-hydro
python scripts/generate_docs_models.py
# → docs/models.md (93) · docs/formulas.md
```

## Local MkDocs build (optional smoke)

```bash
cd packages/sailboat-hydro
python -m pip install -e ".[docs]"   # or: pip install mkdocs
mkdocs build --strict
# output: site/ (gitignored)
```

## Owner · Read the Docs

1. Import project at https://readthedocs.org/ (point at this repo or a split docs repo).
2. Set docs directory / config to `packages/sailboat-hydro/.readthedocs.yaml`.
3. Confirm project slug → expected `https://sailboat-hydro.readthedocs.io/`.
4. Verify `/en/latest/models/` lists **93** FairHelm model links.

## Owner · GitHub Pages (alternate)

```bash
cd packages/sailboat-hydro
mkdocs gh-deploy --force   # owner only; pushes to gh-pages
```

Or upload `site/` to any static host. Keep canonical links pointing at `fairhelm.com`.

## Do not

- Agent `gh-deploy` / RTD webhook fire
- Rewrite model card prose on fairhelm.com from this pack
