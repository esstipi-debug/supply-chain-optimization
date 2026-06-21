"""Generate a sample price/quantity dataset for the pricing playbook.

Each SKU has weekly observations where the price varies (promotions / price
changes) and quantity follows a known constant-elasticity curve plus noise — so
the engine can actually estimate elasticity. Mixes elastic and inelastic SKUs.

Run: python scripts/generate_pricing_sample.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

N_WEEKS = 52
START = date(2024, 1, 1)

# id, base_price, elasticity, unit_cost
SKUS = [
    ("PR-A", 25.0, -2.2, 10.0),
    ("PR-B", 12.0, -1.6, 5.0),
    ("PR-C", 40.0, -0.7, 18.0),  # inelastic
    ("PR-D", 8.0, -3.0, 3.0),    # very elastic
    ("PR-E", 60.0, -1.3, 28.0),
    ("PR-F", 15.0, -0.5, 9.0),   # inelastic
]


def main() -> None:
    rows = []
    for sku_id, base_price, elasticity, cost in SKUS:
        rng = random.Random(hash(sku_id) & 0xFFFFFFFF)
        scale = 1000.0 / (base_price**elasticity)  # ~1000 units at base price
        for i in range(N_WEEKS):
            d = START + timedelta(weeks=i)
            price = round(base_price * rng.uniform(0.7, 1.25), 2)  # weekly price moves
            qty = scale * price**elasticity * rng.uniform(0.9, 1.1)
            rows.append([d.isoformat(), sku_id, max(0, round(qty)), price, cost])

    out_path = Path(__file__).resolve().parents[1] / "data" / "sample_pricing.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "product_id", "quantity", "price", "unit_cost"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows for {len(SKUS)} SKUs -> {out_path}")


if __name__ == "__main__":
    main()
