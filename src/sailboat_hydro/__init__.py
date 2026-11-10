"""sailboat-hydro — FairHelm hydro formulas + bundled Nordic benchmark (Zero-Network)."""

from __future__ import annotations

from sailboat_hydro.benchmark import (
    BenchmarkModel,
    NordicBenchmark,
    load_nordic_benchmark,
)
from sailboat_hydro.formulas import (
    capsize_screening,
    comfort_ratio,
    displacement_length_ratio,
    hull_speed_kn,
    sail_area_displacement,
)

__version__ = "1.0.0"

__all__ = [
    "BenchmarkModel",
    "NordicBenchmark",
    "__version__",
    "capsize_screening",
    "comfort_ratio",
    "displacement_length_ratio",
    "hull_speed_kn",
    "load_nordic_benchmark",
    "sail_area_displacement",
]
