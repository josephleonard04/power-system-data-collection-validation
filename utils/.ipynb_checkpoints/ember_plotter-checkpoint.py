import pandas as pd
import matplotlib.pyplot as plt

def plot_ember_summary(year=2020):
    # --- Load and Prepare Data ---
    df = pd.read_csv("raw/europe_monthly_full_release_long_format.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # --- Validate Year ---
    valid_years = list(range(2015, 2025))
    if year not in valid_years:
        raise ValueError(f"Year must be one of {valid_years}")
    df_year = df[df["Year"] == year]

    # --- Graph 1: Total Electricity Demand (Monthly) ---
    df_demand = df_year[
        (df_year["Category"] == "Electricity demand") &
        (df_year["Variable"] == "Demand") &
        (df_year["Unit"] == "TWh")
    ]
    demand_total = df_demand.groupby("Date")["Value"].sum()

    plt.figure(figsize=(10, 6))
    demand_total.plot(kind='line', marker='o', title=f"Total Electricity Demand in {year}")
    plt.ylabel("Total Demand (TWh)")
    plt.xlabel("Month")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Graph 2: Total Annual Renewable Output per Source ---
    renewable_sources = [
        "Wind", "Solar", "Hydro", "Bioenergy", "Onshore wind", "Other renewables"
    ]

    df_renewable = df_year[
        (df_year["Category"] == "Electricity generation") &
        (df_year["Unit"] == "TWh") &
        (
            df_year["Subcategory"].isin(renewable_sources) |
            df_year["Variable"].isin(renewable_sources)
        )
    ].copy()

    df_renewable["Source"] = df_renewable["Subcategory"].where(
        df_renewable["Subcategory"].isin(renewable_sources),
        df_renewable["Variable"]
    )

    annual_totals = df_renewable.groupby("Source")["Value"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    annual_totals.plot(kind='bar', title=f"Total Renewable Output by Source in {year}")
    plt.ylabel("Total Output (TWh)")
    plt.xlabel("Renewable Type")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # --- Graph 3: Daily Average Renewable Output per Source ---
    df_renewable["DaysInMonth"] = df_renewable["Date"].dt.days_in_month
    df_renewable["DailyAvg"] = df_renewable["Value"] / df_renewable["DaysInMonth"]

    daily_avg_per_source = df_renewable.groupby("Source")["DailyAvg"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    daily_avg_per_source.plot(kind='bar', title=f"Avg Daily Renewable Output by Source in {year}")
    plt.ylabel("Average Daily Output (TWh/day)")
    plt.xlabel("Renewable Type")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
