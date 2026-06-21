# Price Optimization — Demo Co

## Executive summary

Analyzed **6 SKUs**. **4** have a confident price move (raise/lower); 2 are inelastic and 0 lack enough price variation to estimate. Recommendations maximize unit margin under a constant-elasticity demand model fitted to each SKU's price/quantity history.

## Recommended price per SKU

| SKU | Current | Optimal | Unit cost | Elasticity | R² | Obs | Δ demand | Profit uplift | Action | Confident |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| PR-A | $24.30 | $18.67 | $10.00 | -2.15 | 0.98 | 52 | +76% | +7% | Lower price | yes |
| PR-B | $11.39 | $14.94 | $5.00 | -1.50 | 0.95 | 52 | -33% | +3% | Raise price | yes |
| PR-C | $38.28 | — | $18.00 | -0.58 | 0.73 | 52 | — | — | Inelastic — test higher | no |
| PR-D | $7.62 | $4.52 | $3.00 | -2.97 | 0.99 | 52 | +373% | +56% | Lower price | yes |
| PR-E | $58.97 | $123.85 | $28.00 | -1.29 | 0.93 | 52 | -62% | +19% | Raise price | yes |
| PR-F | $14.61 | — | $9.00 | -0.46 | 0.56 | 52 | — | — | Inelastic — test higher | no |

## Methodology

- **Elasticity:** per-SKU log-log regression of quantity on price (ε = slope of ln q vs ln p), with R² as a fit-quality signal.
- **Optimal price:** constant-elasticity profit maximum `p* = c · ε/(ε+1)`, valid when demand is elastic (ε < −1). Inelastic SKUs (ε ≥ −1) have no interior optimum — test a higher price.
- **Profit uplift / demand change:** modeled against the fitted curve relative to the current (median) price.
- **Confidence:** flagged only when R² ≥ 0.5, ≥ 4 price observations, and the move is within a sane range of the current price.

## Assumptions & caveats

- Unit cost taken from the data (no cost column → margin is an estimate).
- A single-product, constant-elasticity model: it ignores cross-product effects, competitor moves, and capacity. Validate before repricing, ideally with a live price test.

_Decision support generated from the client's price/quantity history._