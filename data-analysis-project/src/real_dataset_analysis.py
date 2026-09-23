from __future__ import annotations

from pathlib import Path

import pandas as pd


def normalize_real_dataset(input_path: str | Path) -> pd.DataFrame:
    """Normalize a real retail dataset to the project's standard column names."""
    df = pd.read_csv(input_path)

    column_mapping = {
        "Date": "order_date",
        "Revenue": "sales",
        "Profit": "profit",
        "Store": "store_name",
        "Region": "region",
        "Category": "category",
        "Channel": "channel",
        "Units": "units_sold",
        "Returns": "returns",
    }

    df = df.rename(columns=column_mapping)
    df["order_date"] = pd.to_datetime(df["order_date"])

    expected_order = [
        "order_date",
        "sales",
        "profit",
        "store_name",
        "region",
        "category",
        "channel",
        "units_sold",
        "returns",
    ]
    return df[expected_order]


if __name__ == "__main__":
    sample = Path(__file__).resolve().parents[1] / "data" / "sales_data.csv"
    df = normalize_real_dataset(sample)
    print(df.head())
