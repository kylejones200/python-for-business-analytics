"""Dataset helpers for *Python for Business Analytics* examples.

What you'll learn:
  - How to keep book/example datasets discoverable via a simple YAML catalog
  - How to build (or fetch) missing datasets via a builder script, with clear
    error messages when data is unavailable
  - How to write scripts that are runnable from any working directory using
    `pathlib.Path`
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    path: Path
    format: str | None
    builder: Path | None
    meta: dict[str, Any]


def project_root() -> Path:
    """Return the repository root (directory containing data_catalog.yaml)."""
    here = Path(__file__).resolve()
    root = here.parents[1]
    return root


def _catalog_path() -> Path:
    return project_root() / "data_catalog.yaml"


def load_catalog() -> dict[str, Any]:
    """Load the dataset catalog from `data_catalog.yaml`.

    Returns:
        Parsed YAML catalog as a dictionary with a top-level ``datasets`` mapping.

    Raises:
        FileNotFoundError: If the catalog file is missing.
        ValueError: If the catalog structure is invalid.
    """
    path = _catalog_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Missing data catalog at {path}. Expected `data_catalog.yaml` at project root."
        )

    catalog = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(catalog, dict) or "datasets" not in catalog:
        raise ValueError(f"Invalid catalog format in {path}. Expected top-level `datasets:`.")

    datasets = catalog.get("datasets", {})
    if not isinstance(datasets, dict):
        raise ValueError(f"Invalid catalog format in {path}. Expected `datasets:` to be a mapping.")

    return catalog


def get_dataset_spec(name: str) -> DatasetSpec:
    """Return a validated dataset spec from the catalog.

    Args:
        name: Dataset name as listed under ``datasets:`` in `data_catalog.yaml`.

    Returns:
        A `DatasetSpec` with resolved absolute paths.

    Raises:
        KeyError: If the dataset name is not in the catalog.
        ValueError: If the dataset spec is malformed.
    """
    catalog = load_catalog()
    datasets = catalog["datasets"]
    if name not in datasets:
        raise KeyError(f"Unknown dataset name: {name!r}. Check `data_catalog.yaml`.")

    raw = datasets[name]
    if not isinstance(raw, dict) or "path" not in raw:
        raise ValueError(f"Invalid dataset spec for {name!r} in data_catalog.yaml.")

    root = project_root()
    rel_path = Path(str(raw["path"]))
    ds_path = (root / rel_path).resolve()
    fmt = raw.get("format")
    builder = raw.get("builder")
    builder_path = (root / Path(builder)).resolve() if builder else None

    meta = {k: v for k, v in raw.items() if k not in {"path", "format", "builder"}}
    return DatasetSpec(
        name=name,
        path=ds_path,
        format=str(fmt) if fmt is not None else None,
        builder=builder_path,
        meta=meta,
    )


def get_dataset_path(name: str) -> Path:
    """Return the absolute path to a named dataset (no I/O, no creation)."""
    return get_dataset_spec(name).path


def require_dataset(name: str) -> Path:
    """Return an existing dataset path or raise FileNotFoundError.

    Reader-facing listings must call this (or ``load_frame``) instead of
    treating a missing file as a successful skip.
    """
    path = get_dataset_path(name)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset {name!r} is missing at {path}. "
            "Run `python scripts/make_data.py` from the project root."
        )
    return path


def load_frame(name: str):
    """Load a catalog dataset as a pandas DataFrame."""
    import pandas as pd

    path = require_dataset(name)
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported tabular format for {name!r}: {suffix}")


def load_zip_points(*, crs_epsg: int = 3081):
    """Join zip_income to ZIP centroids on ZCTA5 and project to meters.

    Join on ``ZCTA5CE10``, not ``GEOID10``. GEOID10 prepends the state FIPS
    code, so it will not match a five-digit ZIP.
    """
    import geopandas as gpd
    import pandas as pd

    income = load_frame("zip_income").copy()
    income["zip"] = income["zip"].astype(str).str.zfill(5)
    gdf = gpd.read_file(require_dataset("zip_geometry")).to_crs(crs_epsg)
    gdf = gdf.copy()
    gdf["zip"] = gdf["ZCTA5CE10"].astype(str).str.zfill(5)
    merged = gdf.merge(income, on="zip", how="inner")
    if merged.empty:
        raise ValueError("zip_income does not join zip_geometry on ZCTA5CE10.")
    centroids = merged.geometry.centroid
    return pd.DataFrame(
        {
            "zip": merged["zip"].to_numpy(),
            "easting_m": centroids.x.to_numpy(),
            "northing_m": centroids.y.to_numpy(),
            "median_income_usd": merged["median_income_usd"].to_numpy(),
        }
    )


def ensure_dataset(name: str, *, force: bool = False, quiet: bool = False) -> Path:
    """Ensure a dataset exists locally and return its path.

    Missing data is an error. Reader-facing listings must not treat a missing
    file as a successful skip.

    Args:
        name: Dataset name from `data_catalog.yaml`.
        force: If True, rebuild even if an output file exists.
        quiet: If True, suppress builder error logs (the exception still raises).

    Returns:
        The dataset path.

    Raises:
        FileNotFoundError: If the dataset cannot be created or located.
    """
    spec = get_dataset_spec(name)
    if spec.path.exists() and not force:
        return spec.path

    if spec.builder is None:
        raise FileNotFoundError(
            f"Dataset {name!r} is missing and has no builder in data_catalog.yaml."
        )

    if not spec.builder.exists():
        raise FileNotFoundError(
            f"Builder script for dataset {name!r} not found: {spec.builder}"
        )

    # Run builder as a subprocess to keep listings simple and robust.
    cmd = [sys.executable, str(spec.builder)]
    # Convention: builders accept --only <dataset> and --force.
    cmd += ["--only", name]
    if force:
        cmd += ["--force"]

    env = dict(os.environ)
    # Make it easy for builder scripts to find the project root.
    env["BOOK_PROJECT_ROOT"] = str(project_root())

    try:
        proc = subprocess.run(cmd, cwd=str(project_root()), env=env)
    except Exception as e:
        raise FileNotFoundError(f"Failed running builder for {name!r}: {e}") from e

    if proc.returncode != 0:
        raise FileNotFoundError(
            f"Builder for {name!r} exited with code {proc.returncode}. Tried: {' '.join(cmd)}"
        )

    if not spec.path.exists():
        raise FileNotFoundError(
            f"Builder for {name!r} finished but dataset file still missing: {spec.path}"
        )

    return spec.path


def main() -> None:
    """List available datasets and optionally build one.

    This is a convenience entrypoint so `src/bookdata.py` is runnable as a small
    teaching script.
    """
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="List datasets in data_catalog.yaml and optionally ensure one exists."
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Optional dataset name to build/ensure (e.g., business_ops).",
    )
    parser.add_argument("--force", action="store_true", help="Rebuild if output exists.")
    args = parser.parse_args()

    catalog = load_catalog()
    datasets = catalog.get("datasets", {})
    logger.info("Datasets in catalog (%d): %s", len(datasets), ", ".join(sorted(datasets)))

    if args.name:
        path = ensure_dataset(args.name, force=args.force, quiet=False)
        if path is None:
            raise SystemExit(1)
        logger.info("Dataset ready: %s", path)


if __name__ == "__main__":
    main()