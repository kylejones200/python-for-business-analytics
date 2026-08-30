# Python for Business Analytics — code and data

Companion repository for *Python for Business Analytics* (Kyle T. Jones,
Springer Nature). Every numbered listing in the book is a file here, and the
datasets the listings read ship with the repository, so the printed numbers
reproduce offline.

## Layout

    code/<chapter>/listing-<NN>.py   every numbered listing in the book
    data/                            the packaged tables the listings read
    src/bookdata.py                  loads those tables by name
    src/bookhelpers.py               shared helpers used across chapters
    scripts/                         rebuilds the datasets from their sources
    data_catalog.yaml                what each dataset is and where it came from

Listings are named for their chapter and position, so `code/2.0/listing-17.py`
is the seventeenth listing in Chapter 2.

## Running a listing

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python code/2.0/listing-17.py

Chapter 8 needs the geostatistics extras:

    pip install -r requirements_geostatistics.txt

Every listing that reads the packaged data puts `src/` on `sys.path` itself and
resolves paths relative to the repository root, so run them from anywhere in a
checkout — no install step and no `PYTHONPATH` to set.

## The datasets

From Chapter 2 onward the listings do not download anything. They read a small
set of packaged tables so results do not drift when an external source is
revised:

| dataset | rows | what it is |
|---|---|---|
| `business_customers` | 2,000 | synthetic accounts: segment, industry, region, MRR, NPS, adoption, onboarding, churn flag |
| `business_ops` | 10,000 | synthetic orders: dates, quantities, promised and actual ship days, gross and net value |
| `business_tickets` | — | synthetic support ticket log |
| `fred_series` | — | public macroeconomic series from FRED |
| `zip_income`, `zip_geometry` | — | ZIP-level income joined to ZCTA boundaries |

`data_catalog.yaml` records the provenance of each one and the script under
`scripts/` that rebuilds it. The synthetic tables are generated, not collected:
they describe no real company or person.

Load one by name:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("src")))

from bookdata import load_frame

df = load_frame("business_customers")
```

## Reproducibility

The listings are deterministic. Where a listing draws random numbers it seeds
the generator, so a given listing prints the same figures shown in the book.
Two exceptions print a wall-clock timestamp in a `statsmodels` summary header,
and one prints a set whose element order Python does not fix; the numbers in
both are stable.

## License

Not yet set. The book text is not part of this repository.
