"""Fulfill a price-optimization job from a client price/quantity file.

    python examples/run_pricing_job.py --data sample_pricing.csv
    python examples/run_pricing_job.py --data sales.xlsx --cost-ratio 0.55 --out deliverables/acme-pricing --client "Acme Co"

Pipeline: intake (detect price/quantity columns) -> playbook (elasticity ->
optimal price) -> QA -> deliverables (Excel + report + CSV).
"""

from __future__ import annotations

import argparse
import sys

from jobs import deliverables, qa
from jobs.pricing import prepare_pricing, run


def main() -> int:
    parser = argparse.ArgumentParser(description="Price optimization job from a client price/quantity file.")
    parser.add_argument("--data", required=True, help="client CSV/Excel with price + quantity history")
    parser.add_argument("--out", default="deliverables/pricing", help="output directory")
    parser.add_argument("--client", default="Client")
    parser.add_argument("--period", default="W", help="bucketing period (W weekly, D daily, MS monthly)")
    parser.add_argument("--cost-ratio", type=float, default=0.6, help="assumed cost as fraction of price when no cost column")
    args = parser.parse_args()

    demand = prepare_pricing(args.data, period=args.period)
    print(f"Intake: {demand['product_id'].nunique()} SKUs · {len(demand)} price points from {args.data}")

    report = run(demand, cost_ratio=args.cost_ratio)
    issues = qa.verify_pricing(report)
    if issues:
        print("QA FAILED — deliverables not written:", file=sys.stderr)
        for i in issues:
            print("  - " + i, file=sys.stderr)
        return 1

    written = deliverables.write_pricing_all(report, args.out, client=args.client)
    print(f"QA passed. {report.n_actionable}/{report.n_skus} SKUs with a confident price move "
          f"({report.n_inelastic} inelastic, {report.n_insufficient} insufficient data)")
    for kind, path in written.items():
        print(f"  {kind:7s} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
