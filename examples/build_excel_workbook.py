#!/usr/bin/env python3
"""Build Excel workbook from sample analysis (Vandeput 2020)."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.cost_optimization import optimize_rs_policy
from src.data_loader import annualize_demand, demand_stats, load_demand_csv
from src.eoq import compute_eoq, round_review_period_power_of_two
from src.excel_export import gsm_allocation_to_dict, write_analysis_workbook
from src.multi_echelon import optimize_serial_gsm, simulate_serial_gsm
from src.newsvendor import muffin_pmf, optimal_newsvendor_discrete
from src.policies import continuous_review_sq, periodic_review_rs


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Excel analysis workbook")
    parser.add_argument("--data", type=Path, default=Path("data/sample_demand.csv"))
    parser.add_argument("--product", default="SKU-A")
    parser.add_argument("--output", type=Path, default=Path("excel-templates/inventory-analysis.xlsx"))
    args = parser.parse_args()

    series = load_demand_csv(args.data, product_id=args.product)
    stats = demand_stats(series)
    mu, sigma = stats["mean_demand_per_period"], stats["demand_std_per_period"]
    annual_demand = annualize_demand(mu, 52.0)
    h_year = 1.25 * 52

    eoq = compute_eoq(annual_demand, h_year, 1000.0)
    review = round_review_period_power_of_two(eoq.review_period * 52)
    sq = continuous_review_sq(annual_demand, mu, sigma, h_year, 1000.0, 2.0, 0.95)
    rs = periodic_review_rs(annual_demand, mu, sigma, h_year, 1000.0, 2.0, review, 0.95)
    best_rs = optimize_rs_policy(mu, sigma, 2.0, 1.25, 1000.0, 50.0)
    gsm = optimize_serial_gsm([4, 3, 2], 100, 25, [1, 2, 4], 0.95, 1.0)
    gsm_sim = simulate_serial_gsm(gsm, [4, 3, 2], periods=2000, seed=1)
    nv = optimal_newsvendor_discrete(muffin_pmf(), price=6, unit_cost=2, salvage_value=1)

    path = write_analysis_workbook(
        args.output,
        product_id=args.product,
        parameters={
            "annual_demand": annual_demand,
            "mean_demand_per_period": mu,
            "demand_std": sigma,
            "holding_cost_per_period": 1.25,
            "order_cost": 1000,
            "lead_time": 2,
            "service_level": 0.95,
        },
        results={
            "EOQ Q*": eoq.order_quantity,
            "EOQ cost": eoq.optimal_total_cost,
            "(s,Q) Q": sq.order_quantity,
            "(s,Q) s": sq.reorder_point,
            "(R,S) R": rs.review_period,
            "(R,S) S": rs.order_up_to_level,
            "Optimal R (cost)": best_rs.review_period,
            "Optimal cost/period": best_rs.cost.total,
        },
        gsm=gsm_allocation_to_dict(gsm),
        simulation={
            "GSM fill rate": gsm_sim.fill_rate,
            "GSM mean backorders": gsm_sim.mean_backorders,
            "GSM stockout periods": gsm_sim.stockout_periods,
        },
        newsvendor={
            "Q*": nv.optimal_quantity,
            "critical ratio": nv.critical_ratio,
            "expected profit": nv.expected_profit,
        },
    )
    print(f"Workbook written: {path}")


if __name__ == "__main__":
    main()
