"""Download ZIP geometry GeoJSON and cache it locally.

What you'll learn:
  - How to download a small public GeoJSON file with a timeout
  - How to cache external data to `data/` for reproducible scripts
  - How to handle network failures gracefully (use cache if present)

This script does **not** require an API key.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

logger = logging.getLogger(__name__)


DEFAULT_URL = (
    "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/"
    "master/tx_texas_zip_codes_geo.min.json"
)


def _project_root() -> Path:
    import os

    env_root = os.environ.get("BOOK_PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> None:
    """Download ZIP geometry and write to `data/zip_geometry.geojson`.

    Args:
        argv: Optional CLI args (primarily for testing).
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Download ZIP geometry GeoJSON and cache to data/zip_geometry.geojson."
    )
    parser.add_argument("--only", default="zip_geometry", help="Dataset name (for compatibility).")
    parser.add_argument("--force", action="store_true", help="Overwrite cached output.")
    parser.add_argument("--url", default=DEFAULT_URL, help="GeoJSON source URL.")
    parser.add_argument(
        "--max-features",
        type=int,
        default=1000,
        help="Optional cap on number of features to keep (keeps file small).",
    )
    args = parser.parse_args(argv)

    if args.only not in {"zip_geometry", "all"}:
        logger.info(
            "SKIPPED: fetch_zip_geometry.py only supports --only zip_geometry (got %r).",
            args.only,
        )
        return None

    root = _project_root()
    out_path = root / "data" / "zip_geometry.geojson"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists() and not args.force:
        logger.info("Using cached ZIP geometry: %s", out_path)
        return None

    try:
        with urlopen(args.url, timeout=30) as resp:  # nosec - simple public download
            raw = resp.read()
    except URLError as e:
        if out_path.exists():
            logger.warning(
                "Failed to download ZIP geometry; using existing cache.\nReason: %s", e
            )
            return None
        logger.error("Failed to download ZIP geometry (and no cached file exists).")
        logger.error("URL: %s", args.url)
        logger.error("Reason: %s", e)
        logger.error("Tip: Check your network connection and try again.")
        raise SystemExit(1)
    except Exception as e:
        if out_path.exists():
            logger.warning(
                "Failed to download ZIP geometry; using existing cache.\nReason: %s", e
            )
            return None
        logger.error("Failed to download ZIP geometry (and no cached file exists).")
        logger.error("URL: %s", args.url)
        logger.error("Reason: %s", e)
        raise SystemExit(1)

    try:
        geo = json.loads(raw.decode("utf-8"))
        if (
            isinstance(geo, dict)
            and isinstance(geo.get("features"), list)
            and args.max_features
            and len(geo["features"]) > args.max_features
        ):
            geo["features"] = geo["features"][: args.max_features]
        out_path.write_text(json.dumps(geo), encoding="utf-8")
    except Exception as e:
        logger.error("Downloaded ZIP geometry but failed to parse/write GeoJSON: %s", e)
        raise SystemExit(1)

    kept = None
    try:
        kept = len(geo.get("features", [])) if isinstance(geo, dict) else None
    except Exception:
        kept = None
    kept_str = f"{kept:,}" if isinstance(kept, int) else "?"
    logger.info("Wrote ZIP geometry to %s (features kept: %s)", out_path, kept_str)
    return None


if __name__ == "__main__":
    main()

