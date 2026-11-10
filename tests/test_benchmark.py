"""Bundled Nordic benchmark + Zero-Network guarantees."""

from __future__ import annotations

import ast
from pathlib import Path

from sailboat_hydro import load_nordic_benchmark
from sailboat_hydro.formulas import (
    capsize_screening,
    comfort_ratio,
    displacement_length_ratio,
    hull_speed_kn,
)

SRC_ROOT = Path(__file__).resolve().parents[1] / "src" / "sailboat_hydro"


def test_load_nordic_benchmark_count() -> None:
    bench = load_nordic_benchmark()
    assert bench.model_count == 93
    assert len(bench.models) == 93
    assert bench.zenodo_doi == "https://doi.org/10.5281/zenodo.23374417"
    assert "formulas" in bench.formulas_methodology_url


def test_hr36_row_and_recompute() -> None:
    bench = load_nordic_benchmark()
    hr36 = bench.get("hallberg-rassy", "hr36")
    assert hr36 is not None
    assert hr36.name == "HR 36"
    assert hr36.lwl_m == 9.35
    assert hr36.displacement_kg == 7500
    assert hr36.hull_speed_kn is not None
    assert abs(hr36.hull_speed_kn - 7.43) < 0.01

    assert hr36.lwl_m is not None
    assert hr36.beam_m is not None
    assert hr36.displacement_kg is not None
    assert hr36.loa_m is not None
    recomputed_hs = hull_speed_kn(hr36.lwl_m)
    recomputed_csf = capsize_screening(hr36.beam_m, hr36.displacement_kg)
    recomputed_dl = displacement_length_ratio(hr36.displacement_kg, hr36.lwl_m)
    recomputed_cr = comfort_ratio(
        displacement_kg=hr36.displacement_kg,
        lwl_m=hr36.lwl_m,
        loa_m=hr36.loa_m,
        beam_m=hr36.beam_m,
    )
    assert recomputed_hs is not None and hr36.hull_speed_kn is not None
    assert abs(recomputed_hs - hr36.hull_speed_kn) < 0.02
    assert recomputed_csf is not None and hr36.capsize_screening is not None
    assert abs(recomputed_csf - hr36.capsize_screening) < 0.002
    assert recomputed_dl is not None and hr36.displacement_length_ratio is not None
    assert abs(recomputed_dl - hr36.displacement_length_ratio) < 0.2
    assert recomputed_cr is not None and hr36.comfort_ratio is not None
    assert abs(recomputed_cr - hr36.comfort_ratio) < 0.05


def test_zero_network_no_http_imports() -> None:
    """Hot-path modules must not import networking clients."""
    banned = {
        "urllib",
        "urllib.request",
        "urllib3",
        "requests",
        "http.client",
        "httpx",
        "aiohttp",
        "socket",
    }
    for path in SRC_ROOT.rglob("*.py"):
        if path.name == "__init__.py" and path.parent.name == "data":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    assert alias.name not in banned
                    assert root not in banned
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".")[0]
                assert node.module not in banned
                assert root not in banned
        text = path.read_text(encoding="utf-8")
        assert "api.fairhelm.com" not in text
