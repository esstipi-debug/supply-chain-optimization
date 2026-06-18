# Excel Templates

> **Status:** Python generates `.xlsx` workbooks from analysis results.

Per Vandeput (2020), Excel is best for **visualizing results** and simple what-if checks — Monte Carlo stays in Python.

## Generate workbook

```bash
pip install -r requirements.txt
python examples/build_excel_workbook.py
# -> excel-templates/inventory-analysis.xlsx

python examples/run_complete.py --simulate --excel excel-templates/my-sku.xlsx
```

## Sheets

| Sheet | Content |
|-------|---------|
| Summary | EOQ, policies, optimization results |
| Parameters | Inputs (D, h, k, L, alpha, ...) |
| Formulas | Book reference formulas |
| GSM | Multi-echelon allocation (Ch. 10) |
| Simulation | Sim metrics when `--simulate` |
| Newsvendor | Muffins example (Ch. 11) |

## Excel formulas (manual what-if)

```
EOQ:     =SQRT(2*D*k/h)
z_alpha: =NORM.S.INV(alpha)
Ss:      =NORM.S.INV(alpha)*sigma*SQRT(tau)
```

See [METHODOLOGY.md](../documentation/METHODOLOGY.md) for notation.
