"""Load ZIP geometry and income, join on ZCTA5, then project to meters.

Euclidean distances, variograms, and kriging require projected coordinates
with meaningful units. Do not treat latitude/longitude degrees as meters.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame, load_zip_points, require_dataset

income = load_frame("zip_income")
print("zip_income rows:", len(income))
print(income.head(3).to_string(index=False))

import geopandas as gpd

gdf = gpd.read_file(require_dataset("zip_geometry"))
print("Geometry CRS before projection:", gdf.crs)
print("Join key is ZCTA5CE10, not GEOID10.")
print("GEOID10 sample:", gdf["GEOID10"].head(3).tolist())
print("ZCTA5CE10 sample:", gdf["ZCTA5CE10"].head(3).tolist())

points = load_zip_points(crs_epsg=3081)
print("Inner join on ZCTA5:", len(points), "ZIP codes")
print("Projected CRS: EPSG:3081 (Texas Statewide Mapping System, meters)")
print(
    "Centroid easting range (m): {:.0f} to {:.0f}".format(
        points["easting_m"].min(), points["easting_m"].max()
    )
)
print(
    "Centroid northing range (m): {:.0f} to {:.0f}".format(
        points["northing_m"].min(), points["northing_m"].max()
    )
)
print(points.head(3).to_string(index=False))
print("Later listings use these projected meters, not raw lat/lon degrees.")
