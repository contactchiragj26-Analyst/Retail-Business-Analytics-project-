from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from sql_workflow import export_sql_summary


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sales_data.csv"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"


def load_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int | str]:
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_profit": 0.0,
            "total_units": 0,
            "average_order_value": 0.0,
            "top_region": "N/A",
            "top_channel": "N/A",
            "return_rate_pct": 0.0,
        }

    total_revenue = float(df["sales"].sum())
    total_profit = float(df["profit"].sum())
    total_units = int(df["units_sold"].sum())
    average_order_value = float(df["sales"].mean())
    top_region = df.groupby("region")["sales"].sum().idxmax()
    top_channel = df.groupby("channel")["sales"].sum().idxmax()
    return_rate_pct = (df["returns"].mean() * 100) if "returns" in df.columns else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "total_units": total_units,
        "average_order_value": round(average_order_value, 2),
        "top_region": top_region,
        "top_channel": top_channel,
        "return_rate_pct": round(float(return_rate_pct), 2),
    }


def summarize_by_month(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["order_date"] = pd.to_datetime(working["order_date"])
    monthly = (
        working.assign(month=working["order_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["sales"]
        .sum()
        .rename(columns={"sales": "sales"})
        .set_index("month")
    )
    return monthly.sort_index()


def summarize_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("region", as_index=False)["sales"].sum().sort_values("sales", ascending=False)


def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("category", as_index=False).agg(
        revenue=("sales", "sum"),
        profit=("profit", "sum"),
    ).sort_values("revenue", ascending=False)


def summarize_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("channel", as_index=False).agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
    ).sort_values("sales", ascending=False)


def summarize_by_store(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("store_name", as_index=False).agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
    ).sort_values("sales", ascending=False)


def save_kpis(kpis: dict[str, float | int | str], output_path: str | Path) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([kpis]).to_csv(out, index=False)


def plot_monthly_sales(monthly: pd.DataFrame, output_path: str | Path) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(monthly.index, monthly["sales"], marker="o", linewidth=2.5, color="#2f6fed")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_region_sales(region_summary: pd.DataFrame, output_path: str | Path) -> None:
    plt.figure(figsize=(8, 6))
    plt.bar(region_summary["region"], region_summary["sales"], color="#5b9bd5")
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_category_profit(category_summary: pd.DataFrame, output_path: str | Path) -> None:
    plt.figure(figsize=(8, 6))
    plt.bar(category_summary["category"], category_summary["profit"], color="#3e9c63")
    plt.title("Profit by Category")
    plt.xlabel("Category")
    plt.ylabel("Profit")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_channel_performance(channel_summary: pd.DataFrame, output_path: str | Path) -> None:
    plt.figure(figsize=(8, 6))
    plt.bar(channel_summary["channel"], channel_summary["sales"], color="#ef8b3d")
    plt.title("Sales by Channel")
    plt.xlabel("Channel")
    plt.ylabel("Sales")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_store_performance(store_summary: pd.DataFrame, output_path: str | Path) -> None:
    plt.figure(figsize=(9, 6))
    plt.bar(store_summary["store_name"], store_summary["sales"], color="#8e5cf5")
    plt.title("Top Stores by Revenue")
    plt.xlabel("Store")
    plt.ylabel("Sales")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def create_dashboard_html(kpis: dict[str, float | int | str], monthly: pd.DataFrame, region_summary: pd.DataFrame, category_summary: pd.DataFrame, channel_summary: pd.DataFrame, store_summary: pd.DataFrame, output_path: str | Path) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    def format_money(value: float) -> str:
        return f"${value:,.2f}"

    monthly_table = "".join(
        f"<tr><td>{label}</td><td>{format_money(value)}</td></tr>"
        for label, value in zip(monthly.index, monthly["sales"].tolist())
    )
    region_rows = "".join(
        f"<tr><td>{row['region']}</td><td>{format_money(row['sales'])}</td></tr>"
        for _, row in region_summary.head(5).iterrows()
    )
    category_rows = "".join(
        f"<tr><td>{row['category']}</td><td>{format_money(row['profit'])}</td></tr>"
        for _, row in category_summary.head(4).iterrows()
    )
    channel_rows = "".join(
        f"<tr><td>{row['channel']}</td><td>{format_money(row['sales'])}</td></tr>"
        for _, row in channel_summary.head(4).iterrows()
    )
    store_rows = "".join(
        f"<tr><td>{row['store_name']}</td><td>{format_money(row['sales'])}</td></tr>"
        for _, row in store_summary.head(5).iterrows()
    )

    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
      <meta charset=\"UTF-8\" />
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
      <title>Retail Performance Dashboard</title>
      <style>
        :root {{
          --bg: #f4f7fb;
          --panel: #ffffff;
          --title: #172033;
          --muted: #627085;
          --primary: #2f6fed;
          --primary-soft: #eaf1ff;
          --green: #2f9e68;
          --orange: #ef8b3d;
          --purple: #8e5cf5;
          --border: #e7edf5;
        }}
        body {{ font-family: Arial, sans-serif; margin: 0; background: linear-gradient(180deg, #eff4ff 0%, var(--bg) 70%); color: var(--title); }}
        .container {{ max-width: 1200px; margin: 40px auto; padding: 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }}
        .title {{ font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em; }}
        .subtitle {{ color: var(--muted); margin-top: 6px; font-size: 1rem; }}
        .summary-note {{ background: var(--primary-soft); border: 1px solid #d7e5ff; border-radius: 12px; padding: 12px 16px; color: #21448a; margin-bottom: 18px; font-weight: 600; }}
        .cards {{ display: grid; grid-template-columns: repeat(5, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .card {{ background: var(--panel); border-radius: 14px; padding: 20px; box-shadow: 0 8px 22px rgba(34, 61, 106, 0.06); border: 1px solid var(--border); }}
        .card-label {{ color: var(--muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }}
        .card-value {{ font-size: 1.8rem; font-weight: 800; margin-top: 8px; }}
        .grid {{ display: grid; grid-template-columns: 1.35fr 1fr; gap: 20px; }}
        .panel {{ background: var(--panel); border-radius: 14px; padding: 18px; box-shadow: 0 8px 22px rgba(34, 61, 106, 0.05); border: 1px solid var(--border); }}
        h3 {{ margin-top: 0; margin-bottom: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--border); }}
        th {{ color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; }}
        @media (max-width: 900px) {{
          .cards {{ grid-template-columns: repeat(2, minmax(160px, 1fr)); }}
          .grid {{ grid-template-columns: 1fr; }}
        }}
      </style>
    </head>
    <body>
      <div class=\"container\">
        <div class=\"header\">
          <div>
            <div class=\"title\">Retail Performance Dashboard</div>
            <div class=\"subtitle\">Portfolio view of revenue, profit, channel efficiency, and risk</div>
          </div>
        </div>

        <div class=\"summary-note\">
          Key insight: the strongest retail performance is driven by {kpis['top_region']} demand and {kpis['top_channel']} sales, while the return rate remains manageable at {float(kpis['return_rate_pct']):.2f}%.
        </div>

        <div class=\"cards\">
          <div class=\"card\"><div class=\"card-label\">Revenue</div><div class=\"card-value\">{format_money(float(kpis['total_revenue']))}</div></div>
          <div class=\"card\"><div class=\"card-label\">Profit</div><div class=\"card-value\">{format_money(float(kpis['total_profit']))}</div></div>
          <div class=\"card\"><div class=\"card-label\">Units Sold</div><div class=\"card-value\">{int(kpis['total_units'])}</div></div>
          <div class=\"card\"><div class=\"card-label\">AOV</div><div class=\"card-value\">{format_money(float(kpis['average_order_value']))}</div></div>
          <div class=\"card\"><div class=\"card-label\">Return Rate</div><div class=\"card-value\">{float(kpis['return_rate_pct']):.2f}%</div></div>
        </div>

        <div class=\"grid\">
          <div class=\"panel\">
            <h3>Monthly Revenue</h3>
            <table>
              <thead>
                <tr><th>Month</th><th>Sales</th></tr>
              </thead>
              <tbody>
                {monthly_table}
              </tbody>
            </table>
          </div>
          <div class=\"panel\">
            <h3>Top Regions</h3>
            <table>
              <thead><tr><th>Region</th><th>Sales</th></tr></thead>
              <tbody>{region_rows}</tbody>
            </table>
          </div>
        </div>

        <div class=\"grid\" style=\"margin-top: 20px;\">
          <div class=\"panel\">
            <h3>Best Categories by Profit</h3>
            <table>
              <thead><tr><th>Category</th><th>Profit</th></tr></thead>
              <tbody>{category_rows}</tbody>
            </table>
          </div>
          <div class=\"panel\">
            <h3>Sales by Channel</h3>
            <table>
              <thead><tr><th>Channel</th><th>Sales</th></tr></thead>
              <tbody>{channel_rows}</tbody>
            </table>
          </div>
        </div>

        <div class=\"panel\" style=\"margin-top: 20px;\">
          <h3>Top Stores by Revenue</h3>
          <table>
            <thead><tr><th>Store</th><th>Sales</th></tr></thead>
            <tbody>{store_rows}</tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
    """

    out.write_text(html, encoding="utf-8")


def create_interactive_dashboard(df: pd.DataFrame, output_path: str | Path) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data_json = df.to_json(orient="records", date_format="iso")
    regions = ["All"] + sorted(df["region"].unique().tolist())
    categories = ["All"] + sorted(df["category"].unique().tolist())
    channels = ["All"] + sorted(df["channel"].unique().tolist())

    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
      <meta charset=\"UTF-8\" />
      <title>Interactive Sales Dashboard</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #f2f5fa; color: #1f2d3d; }}
        .container {{ max-width: 1100px; margin: 32px auto; padding: 20px; }}
        .controls {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }}
        .filter {{ display: flex; flex-direction: column; font-size: 0.85rem; color: #5d6b82; }}
        select {{ padding: 8px 12px; border-radius: 8px; border: 1px solid #d5dbe4; }}
        .cards {{ display: grid; grid-template-columns: repeat(4, minmax(180px, 1fr)); gap: 16px; margin-bottom: 20px; }}
        .card {{ background: white; border-radius: 12px; padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); }}
        .label {{ color: #697a90; font-size: 0.8rem; text-transform: uppercase; }}
        .value {{ margin-top: 8px; font-weight: 700; font-size: 1.8rem; }}
        table {{ width: 100%; background: white; border-collapse: collapse; border-radius: 12px; overflow: hidden; }}
        th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #edf1f4; }}
        th {{ background: #eef4ff; }}
      </style>
    </head>
    <body>
      <div class=\"container\">
        <h1>Interactive Sales Dashboard</h1>
        <div class=\"controls\">
          <div class=\"filter\">
            <label for=\"regionFilter\">Region</label>
            <select id=\"regionFilter\">
              {''.join(f'<option value="{value}">{value}</option>' for value in regions)}
            </select>
          </div>
          <div class=\"filter\">
            <label for=\"categoryFilter\">Category</label>
            <select id=\"categoryFilter\">
              {''.join(f'<option value="{value}">{value}</option>' for value in categories)}
            </select>
          </div>
          <div class=\"filter\">
            <label for=\"channelFilter\">Channel</label>
            <select id=\"channelFilter\">
              {''.join(f'<option value="{value}">{value}</option>' for value in channels)}
            </select>
          </div>
        </div>
        <div class=\"cards\">
          <div class=\"card\"><div class=\"label\">Revenue</div><div class=\"value\" id=\"totalRevenue\">$0</div></div>
          <div class=\"card\"><div class=\"label\">Profit</div><div class=\"value\" id=\"totalProfit\">$0</div></div>
          <div class=\"card\"><div class=\"label\">Units</div><div class=\"value\" id=\"totalUnits\">0</div></div>
          <div class=\"card\"><div class=\"label\">Return Rate</div><div class=\"value\" id=\"returnRate\">0%</div></div>
        </div>
        <table>
          <thead>
            <tr><th>Region</th><th>Category</th><th>Channel</th><th>Sales</th><th>Profit</th></tr>
          </thead>
          <tbody id=\"tableBody\"></tbody>
        </table>
      </div>
      <script>
        const data = {data_json};
        const regionFilter = document.getElementById('regionFilter');
        const categoryFilter = document.getElementById('categoryFilter');
        const channelFilter = document.getElementById('channelFilter');

        function currency(value) {{ return '$' + Number(value).toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}); }}

        function updateDashboard() {{
          const region = regionFilter.value;
          const category = categoryFilter.value;
          const channel = channelFilter.value;

          const filtered = data.filter(row => {{
            const regionMatch = region === 'All' || row.region === region;
            const categoryMatch = category === 'All' || row.category === category;
            const channelMatch = channel === 'All' || row.channel === channel;
            return regionMatch && categoryMatch && channelMatch;
          }});

          const totalRevenue = filtered.reduce((sum, row) => sum + Number(row.sales), 0);
          const totalProfit = filtered.reduce((sum, row) => sum + Number(row.profit), 0);
          const totalUnits = filtered.reduce((sum, row) => sum + Number(row.units_sold), 0);
          const returnRate = filtered.length ? (filtered.filter(row => Number(row.returns) === 1).length / filtered.length) * 100 : 0;

          document.getElementById('totalRevenue').textContent = currency(totalRevenue);
          document.getElementById('totalProfit').textContent = currency(totalProfit);
          document.getElementById('totalUnits').textContent = totalUnits.toLocaleString();
          document.getElementById('returnRate').textContent = returnRate.toFixed(2) + '%';

          const rows = filtered.slice(0, 10).map(row => `
            <tr>
              <td>${{row.region}}</td>
              <td>${{row.category}}</td>
              <td>${{row.channel}}</td>
              <td>${{currency(row.sales)}}</td>
              <td>${{currency(row.profit)}}</td>
            </tr>
          `).join('');

          document.getElementById('tableBody').innerHTML = rows || '<tr><td colspan="5">No matching data</td></tr>';
        }}

        [regionFilter, categoryFilter, channelFilter].forEach(element => element.addEventListener('change', updateDashboard));
        updateDashboard();
      </script>
    </body>
    </html>
    """

    out.write_text(html, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    kpis = calculate_kpis(df)
    monthly = summarize_by_month(df)
    region_summary = summarize_by_region(df)
    category_summary = summarize_by_category(df)
    channel_summary = summarize_by_channel(df)
    store_summary = summarize_by_store(df)

    save_kpis(kpis, OUTPUT_DIR / "kpi_summary.csv")
    export_sql_summary(DATA_PATH, OUTPUT_DIR / "sql_summary.csv")
    plot_monthly_sales(monthly, OUTPUT_DIR / "monthly_sales.png")
    plot_region_sales(region_summary, OUTPUT_DIR / "sales_by_region.png")
    plot_category_profit(category_summary, OUTPUT_DIR / "category_profit.png")
    plot_channel_performance(channel_summary, OUTPUT_DIR / "channel_performance.png")
    plot_store_performance(store_summary, OUTPUT_DIR / "store_performance.png")
    create_dashboard_html(kpis, monthly, region_summary, category_summary, channel_summary, store_summary, OUTPUT_DIR / "dashboard.html")
    create_interactive_dashboard(df, OUTPUT_DIR / "dashboard_interactive.html")

    print("Data analysis completed.")
    print(f"Total revenue: ${kpis['total_revenue']:,.2f}")
    print(f"Total profit: ${kpis['total_profit']:,.2f}")
    print(f"Average order value: ${kpis['average_order_value']:,.2f}")
    print(f"Top region: {kpis['top_region']}")
    print(f"Top channel: {kpis['top_channel']}")
    print(f"Return rate: {kpis['return_rate_pct']:.2f}%")


if __name__ == "__main__":
    main()
