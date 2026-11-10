"""Parity checks vs mcp-yacht-specs / FairHelm formula SSOT."""

from __future__ import annotations

import math

from sailboat_hydro import (
    capsize_screening,
    comfort_ratio,
    displacement_length_ratio,
    hull_speed_kn,
    sail_area_displacement,
)


def test_hull_speed_hr36() -> None:
    # HR 36 LWL 9.35 m → snapshot hull_speed_kn 7.43
    assert hull_speed_kn(9.35) is not None
    assert abs(hull_speed_kn(9.35) - 7.43) < 0.01  # type: ignore[operator]


def test_csf_hr36() -> None:
    value = capsize_screening(3.55, 7500)
    assert value is not None
    assert abs(value - 1.829) < 0.002


def test_dl_hr36() -> None:
    value = displacement_length_ratio(7500, 9.35)
    assert value is not None
    assert abs(value - 255.7) < 0.1


def test_comfort_hr36() -> None:
    value = comfort_ratio(
        displacement_kg=7500,
        lwl_m=9.35,
        loa_m=10.87,
        beam_m=3.55,
    )
    assert value is not None
    assert abs(value - 29.97) < 0.05


def test_sad_bavaria_c38() -> None:
    value = sail_area_displacement(79.3, 9070)
    assert value is not None
    assert abs(value - 18.53) < 0.02


def test_invalid_inputs_return_none() -> None:
    assert hull_speed_kn(0) is None
    assert hull_speed_kn(-1) is None
    assert capsize_screening(0, 1000) is None
    assert displacement_length_ratio(1000, 0) is None
    assert sail_area_displacement(0, 1000) is None
    assert comfort_ratio(
        displacement_kg=0, lwl_m=9.0, loa_m=10.0, beam_m=3.0
    ) is None


def test_hull_speed_formula_constant() -> None:
    lwl = 10.0
    expected = 2.43 * math.sqrt(lwl)
    assert hull_speed_kn(lwl) == expected
