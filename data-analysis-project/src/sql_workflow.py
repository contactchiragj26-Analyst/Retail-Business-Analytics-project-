from __future__ import annotations

import csv
from pathlib import Path


def summarize_sql_metrics(rows: list[dict]) -> dict:
    if not rows:
        return {
            "total_revenue": 0.0,
            "total_profit": 0.0,
            "return_rate_pct": 0.0,
            "order_count": 0,
        }

    total_revenue = round(sum(float(row.get("sales", 0)) for row in rows), 2)
    total_profit = round(sum(float(row.get("profit", 0)) for row in rows), 2)
    return_count = sum(int(row.get("returns", 0)) for row in rows)
    order_count = len(rows)
    return_rate_pct = round((return_count / order_count) * 100, 2)

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "return_rate_pct": return_rate_pct,
        "order_count": order_count,
    }


def export_sql_summary(input_csv: str | Path, output_csv: str | Path) -> dict:
    input_path = Path(input_csv)
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    summary = summarize_sql_metrics(rows)

    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["total_revenue", "total_profit", "return_rate_pct", "order_count"])
        writer.writeheader()
        writer.writerow(summary)

    return summary


if __name__ == "__main__":
    export_sql_summary(
        Path(__file__).resolve().parents[1] / "data" / "sales_data.csv",
        Path(__file__).resolve().parents[1] / "output" / "sql_summary.csv",
    )
    print("SQL-style summary exported.")
