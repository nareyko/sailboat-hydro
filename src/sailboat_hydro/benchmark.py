"""Bundled Open European & Nordic Sailboat Benchmark (93 models).

Data ships inside the wheel. ``load_nordic_benchmark()`` reads a package
resource only — Zero-Network (no remote API calls in the hot path).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any


@dataclass(frozen=True, slots=True)
class BenchmarkModel:
    """One yacht row from the bundled Nordic/European benchmark."""

    brand_slug: str
    model_slug: str
    name: str
    loa_m: float | None
    lwl_m: float | None
    beam_m: float | None
    draft_m: float | None
    displacement_kg: float | None
    ballast_kg: float | None
    sail_area_m2: float | None
    production_start_year: int | None
    production_end_year: int | None
    designer: str | None
    keel_type: str | None
    rig_type: str | None
    hull_speed_kn: float | None
    capsize_screening: float | None
    comfort_ratio: float | None
    displacement_length_ratio: float | None
    sail_area_displacement: float | None
    survey_checkpoints: tuple[str, ...]
    canonical_model_url: str
    formulas_methodology_url: str
    survey_service_url: str

    @property
    def key(self) -> str:
        return f"{self.brand_slug}/{self.model_slug}"


@dataclass(frozen=True, slots=True)
class NordicBenchmark:
    """Full bundled snapshot metadata + models."""

    schema_version: int
    generated_at: str
    source: str
    zenodo_doi: str
    formulas_methodology_url: str
    open_data_url: str
    model_count: int
    formulas: tuple[dict[str, str], ...]
    models: tuple[BenchmarkModel, ...]

    def get(self, brand_slug: str, model_slug: str) -> BenchmarkModel | None:
        key = f"{brand_slug}/{model_slug}"
        for model in self.models:
            if model.key == key:
                return model
        return None


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _as_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _parse_model(raw: dict[str, Any]) -> BenchmarkModel:
    coeffs = raw.get("coefficients") or {}
    links = raw.get("links") or {}
    checkpoints = raw.get("survey_checkpoints") or []
    return BenchmarkModel(
        brand_slug=str(raw["brand_slug"]),
        model_slug=str(raw["model_slug"]),
        name=str(raw["name"]),
        loa_m=_as_float(raw.get("loa_m")),
        lwl_m=_as_float(raw.get("lwl_m")),
        beam_m=_as_float(raw.get("beam_m")),
        draft_m=_as_float(raw.get("draft_m")),
        displacement_kg=_as_float(raw.get("displacement_kg")),
        ballast_kg=_as_float(raw.get("ballast_kg")),
        sail_area_m2=_as_float(raw.get("sail_area_m2")),
        production_start_year=_as_int(raw.get("production_start_year")),
        production_end_year=_as_int(raw.get("production_end_year")),
        designer=(str(raw["designer"]) if raw.get("designer") is not None else None),
        keel_type=(str(raw["keel_type"]) if raw.get("keel_type") is not None else None),
        rig_type=(str(raw["rig_type"]) if raw.get("rig_type") is not None else None),
        hull_speed_kn=_as_float(coeffs.get("hull_speed_kn")),
        capsize_screening=_as_float(coeffs.get("capsize_screening")),
        comfort_ratio=_as_float(coeffs.get("comfort_ratio")),
        displacement_length_ratio=_as_float(coeffs.get("displacement_length_ratio")),
        sail_area_displacement=_as_float(coeffs.get("sail_area_displacement")),
        survey_checkpoints=tuple(str(x) for x in checkpoints),
        canonical_model_url=str(links.get("canonical_model_url") or ""),
        formulas_methodology_url=str(
            links.get("formulas_methodology_url")
            or "https://fairhelm.com/en/yachts/formulas/"
        ),
        survey_service_url=str(
            links.get("survey_service_url")
            or "https://fairhelm.com/en/yachts/services/listing-review/"
        ),
    )


@lru_cache(maxsize=1)
def load_nordic_benchmark() -> NordicBenchmark:
    """Load the bundled 93-model Nordic/European sailboat benchmark.

    Reads only the package data file. Does not open sockets or call
    remote FairHelm APIs.
    """
    data_file = resources.files("sailboat_hydro").joinpath("data/nordic_benchmark.json")
    with data_file.open("r", encoding="utf-8") as fh:
        payload: dict[str, Any] = json.load(fh)

    models = tuple(_parse_model(m) for m in payload["models"])
    formulas = tuple(dict(f) for f in payload.get("formulas", []))
    return NordicBenchmark(
        schema_version=int(payload.get("schema_version", 1)),
        generated_at=str(payload.get("generated_at", "")),
        source=str(payload.get("source", "")),
        zenodo_doi=str(
            payload.get("zenodo_doi", "https://doi.org/10.5281/zenodo.23374417")
        ),
        formulas_methodology_url=str(
            payload.get(
                "formulas_methodology_url",
                "https://fairhelm.com/en/yachts/formulas/",
            )
        ),
        open_data_url=str(
            payload.get(
                "open_data_url",
                "https://fairhelm.com/open-data/yacht-specs/v1/openapi.yaml",
            )
        ),
        model_count=int(payload.get("model_count", len(models))),
        formulas=formulas,
        models=models,
    )
