"""Local FairHelm hydro formulas.

Parity with ``packages/mcp-yacht-specs/src/formulas.ts`` and the frontend
formula-interactive SSOT. Pure math only — no HTTP, no CapEx.
"""

from __future__ import annotations

import math


def hull_speed_kn(lwl_m: float) -> float | None:
    """Theoretical hull speed in knots from waterline length in metres.

    ``V = 2.43 * sqrt(LWL_m)``
    """
    if not (lwl_m > 0):
        return None
    return 2.43 * math.sqrt(lwl_m)


def capsize_screening(beam_m: float, displacement_kg: float) -> float | None:
    """Capsize Screening Formula (CSF).

    ``CSF = Beam_m / (Disp_kg / 1025) ** (1/3)``
    """
    if not (beam_m > 0) or not (displacement_kg > 0):
        return None
    return float(beam_m / (displacement_kg / 1025) ** (1 / 3))


def comfort_ratio(
    *,
    displacement_kg: float,
    lwl_m: float,
    loa_m: float,
    beam_m: float,
) -> float | None:
    """Ted Brewer comfort ratio (imperial intermediate units, SI inputs)."""
    if not (
        displacement_kg > 0 and lwl_m > 0 and loa_m > 0 and beam_m > 0
    ):
        return None
    disp_lb = displacement_kg * 2.20462
    lwl_ft = lwl_m * 3.28084
    loa_ft = loa_m * 3.28084
    beam_ft = beam_m * 3.28084
    denom = 0.65 * (0.7 * lwl_ft + 0.3 * loa_ft) * beam_ft**1.333
    if denom <= 0:
        return None
    return float(disp_lb / denom)


def displacement_length_ratio(disp_kg: float, lwl_m: float) -> float | None:
    """Displacement / length ratio (D/L) from SI inputs.

    ``D/L = (Disp_kg / LWL_m^3) * 27.87``
    """
    if not (disp_kg > 0 and lwl_m > 0):
        return None
    return (disp_kg / lwl_m**3) * 27.87


def sail_area_displacement(sa_m2: float, disp_kg: float) -> float | None:
    """Sail area / displacement ratio (SA/D) from SI inputs.

    ``SA/D = (SA_m2 * 101.65) / Disp_kg ** (2/3)``
    """
    if not (sa_m2 > 0 and disp_kg > 0):
        return None
    return float((sa_m2 * 101.65) / disp_kg ** (2 / 3))
