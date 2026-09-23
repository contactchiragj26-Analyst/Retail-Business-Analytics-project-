from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from analyze_sales import calculate_kpis, summarize_by_month


def test_calculate_kpis():
    df = pd.DataFrame(
        {
            "sales": [100.0, 200.0, 300.0],
            "profit": [20.0, 30.0, 60.0],
            "units_sold": [10, 20, 30],
            "region": ["North", "South", "North"],
            "channel": ["Online", "Retail", "Online"],
            "returns": [0, 1, 0],
            "order_date": ["2025-01-05", "2025-02-06", "2025-02-20"],
        }
    )

    kpis = calculate_kpis(df)

    assert kpis["total_revenue"] == 600.0
    assert kpis["total_profit"] == 110.0
    assert kpis["total_units"] == 60
    assert kpis["average_order_value"] == 200.0
    assert kpis["top_region"] == "North"
    assert kpis["top_channel"] == "Online"
    assert round(kpis["return_rate_pct"], 2) == 33.33


def test_summarize_by_month():
    df = pd.DataFrame(
        {
            "sales": [100.0, 150.0, 250.0],
            "order_date": ["2025-01-03", "2025-01-15", "2025-02-10"],
        }
    )

    monthly = summarize_by_month(df)

    assert monthly.loc["2025-01", "sales"] == 250.0
    assert monthly.loc["2025-02", "sales"] == 250.0
