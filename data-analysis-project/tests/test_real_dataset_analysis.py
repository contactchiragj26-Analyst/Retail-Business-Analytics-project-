from pathlib import Path

import pandas as pd

from real_dataset_analysis import normalize_real_dataset


def test_normalize_real_dataset_renames_and_parses_columns(tmp_path):
    input_path = tmp_path / "retail.csv"
    pd.DataFrame(
        {
            "Date": ["2025-01-05", "2025-02-06"],
            "Revenue": [100.0, 250.0],
            "Profit": [20.0, 55.0],
            "Store": ["North Plaza", "South Market"],
            "Region": ["North", "South"],
            "Category": ["Electronics", "Apparel"],
            "Channel": ["Online", "In-Store"],
            "Units": [10, 12],
            "Returns": [0, 1],
        }
    ).to_csv(input_path, index=False)

    df = normalize_real_dataset(input_path)

    assert list(df.columns) == [
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
    assert str(df["order_date"].dtype).startswith("datetime64")
    assert df["sales"].sum() == 350.0
