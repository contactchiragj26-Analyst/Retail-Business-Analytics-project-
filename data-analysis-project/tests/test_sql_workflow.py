from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from sql_workflow import summarize_sql_metrics


def test_summarize_sql_metrics():
    rows = [
        {"order_id": "A1", "sales": 120.0, "profit": 35.0, "returns": 0},
        {"order_id": "A2", "sales": 80.0, "profit": 10.0, "returns": 1},
        {"order_id": "A3", "sales": 200.0, "profit": 60.0, "returns": 0},
    ]

    summary = summarize_sql_metrics(rows)

    assert summary["total_revenue"] == 400.0
    assert summary["total_profit"] == 105.0
    assert summary["return_rate_pct"] == 33.33
