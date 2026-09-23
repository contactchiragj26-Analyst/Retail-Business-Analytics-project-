# 📊 Retail Business Analytics Portfolio Project

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20HTML-0A66C2)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Portfolio](https://img.shields.io/badge/Portfolio-Ready-FF6B6B)](#-why-this-is-portfolio-ready)

A polished retail analytics project designed to showcase business analysis, KPI reporting, dashboard storytelling, and SQL-style data summarization in one reproducible workflow.

```mermaid
flowchart LR
    A[Raw Retail Data] --> B[Clean & Standardize]
    B --> C[Business KPI Analysis]
    C --> D[Charts & Dashboards]
    D --> E[Actionable Insights]
```

## 🚀 Executive summary

This project analyzes a realistic retail sales dataset to answer key business questions such as:

- Which regions and stores are driving the most sales?
- Which categories and channels are most profitable?
- How is revenue trending over time?
- Where is operational risk visible through return behavior?
- Which business decisions are supported by the data?

The final output is a presentation-ready analytics package that can be used in an interview, portfolio, or stakeholder review.

## 📈 Key business insights

The current generated dataset supports the following sample findings:

- Total revenue: $1,001,732.87
- Total profit: $199,944.48
- Average order value: $1,252.17
- Best-performing region: North
- Best-performing sales channel: Wholesale
- Return rate: 9.00%

These metrics illustrate how a business analyst can turn raw transaction data into operational insight and decision support.

## 🧩 What this project includes

- Synthetic but realistic retail sales data with stores, regions, categories, channels, and customer segments
- KPI analysis including revenue, profit, return rate, and order value
- Monthly, regional, category, and channel performance summaries
- Executive-style static dashboards and interactive dashboard outputs
- SQL-style aggregation logic for business-ready summaries
- Notebook walkthrough for presentation and learning
- Automated tests for the core logic

## 🛠️ Tech stack

- Python
- Pandas
- Matplotlib
- Seaborn
- HTML/CSS/JavaScript for dashboard presentation
- Pytest for validation

## 📁 Project structure

- `data/` — generated retail sales dataset
- `src/` — data generation, analysis, SQL workflow, and dashboard scripts
- `notebooks/` — notebook version of the workflow
- `tests/` — validation for KPI and summary logic
- `output/` — generated CSV, chart, and dashboard outputs

## ⚙️ Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Generate the dataset:

```powershell
python src/generate_sample_data.py
```

4. Run the full analysis pipeline:

```powershell
python src/analyze_sales.py
```

5. Run the SQL helper workflow directly when needed:

```powershell
python src/sql_workflow.py
```

## 📦 Output files generated

- `output/kpi_summary.csv`
- `output/sql_summary.csv`
- `output/monthly_sales.png`
- `output/sales_by_region.png`
- `output/category_profit.png`
- `output/channel_performance.png`
- `output/store_performance.png`
- `output/dashboard.html`
- `output/dashboard_interactive.html`

## ❓ Business questions answered

- Which region generates the highest sales volume?
- Which category delivers the strongest profit contribution?
- Which sales channels are performing best?
- Which stores are top contributors to revenue?
- How is sales trending over time?
- What is the return rate and how does it affect margin?
- Which customer and store segments deserve further focus?

## 🧠 Portfolio narrative

This project demonstrates the kind of analysis a business analyst would perform to support retail performance decisions. It moves from raw transaction data to KPI summaries, comparisons, and visual insight generation. The end result is an actionable story for stakeholders: where performance is strong, where risk exists, and where growth opportunities may be worth pursuing.

## ✅ Why this is portfolio-ready

- Clear business context and decision-making value
- Reproducible analysis workflow
- Executive-friendly visualization and dashboards
- Insight-driven storytelling for leadership review
- Strong demonstration of Python analytics and reporting skills

## 💬 Suggested interview talking points

- Explain how the dataset was generated and why it is realistic for retail analysis.
- Walk through KPI definitions and how they help measure performance.
- Describe which business questions the dashboard answers.
- Show how SQL-style aggregation logic supports the same insights in a structured workflow.
- Highlight the importance of return behavior and margin management in revenue reporting.

## 🌱 Next steps

Potential next enhancements include:

- Adding a real-world dataset instead of synthetic data
- Expanding the analysis to customer lifetime value and retention
- Creating a deployed dashboard with filters and drill-downs
- Integrating forecasting and scenario modeling
