from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_sample_data(output_path: str | Path, rows: int = 800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    regions = ["North", "South", "East", "West"]
    cities = {
        "North": ["Toronto", "Chicago"],
        "South": ["Miami", "Dallas"],
        "East": ["New York", "Boston"],
        "West": ["Seattle", "Los Angeles"],
    }
    store_names = ["Urban Mart", "Trend Hub", "Prime Market", "Value Cart", "Daily Basket", "QuickStop"]
    categories = ["Electronics", "Home Goods", "Apparel", "Beauty", "Groceries"]
    channels = ["Online", "In-Store", "Wholesale", "Marketplace"]
    customer_segments = ["New", "Returning", "VIP"]

    record_list = []
    start_date = pd.Timestamp("2024-01-01")
    end_date = pd.Timestamp("2025-06-30")
    all_dates = pd.date_range(start=start_date, end=end_date, freq="D")

    for idx in range(rows):
        order_date = rng.choice(all_dates)
        region = rng.choice(regions)
        city = rng.choice(cities[region])
        store_name = rng.choice(store_names)
        category = rng.choice(categories)
        channel = rng.choice(channels)
        customer_segment = rng.choice(customer_segments)
        units_sold = int(rng.integers(1, 18))

        base_multiplier = {
            "Electronics": 135,
            "Home Goods": 110,
            "Apparel": 90,
            "Beauty": 75,
            "Groceries": 65,
        }[category]

        channel_multiplier = {
            "Online": 1.15,
            "In-Store": 1.0,
            "Wholesale": 1.32,
            "Marketplace": 1.08,
        }[channel]

        region_multiplier = {
            "North": 1.18,
            "South": 0.96,
            "East": 1.1,
            "West": 1.25,
        }[region]

        segment_multiplier = {
            "New": 0.92,
            "Returning": 1.08,
            "VIP": 1.35,
        }[customer_segment]

        sales = round((base_multiplier * units_sold * channel_multiplier * region_multiplier * segment_multiplier), 2)
        profit_margin = {
            "Electronics": 0.22,
            "Home Goods": 0.18,
            "Apparel": 0.16,
            "Beauty": 0.2,
            "Groceries": 0.25,
        }[category]
        profit = round(sales * profit_margin, 2)
        return_flag = rng.random() < 0.09

        record_list.append(
            {
                "order_id": f"ORD-{idx + 1001}",
                "customer_id": f"CUST-{rng.integers(1000, 9999)}",
                "order_date": order_date,
                "store_name": store_name,
                "city": city,
                "region": region,
                "category": category,
                "channel": channel,
                "customer_segment": customer_segment,
                "units_sold": units_sold,
                "sales": sales,
                "profit": profit,
                "returns": int(return_flag),
            }
        )

    df = pd.DataFrame(record_list)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return df


if __name__ == "__main__":
    generate_sample_data(Path(__file__).resolve().parents[1] / "data" / "sales_data.csv")
    print("Realistic e-commerce sales dataset generated.")
