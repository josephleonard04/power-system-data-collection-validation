import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Literal

# Load OPSD 60min CSV with datetime parsing
def _read_opsd_60min_csv(fp: str | Path) -> pd.DataFrame:
    """
    Load OPSD 60-minute dataset and parse timestamps.
    """
    df = pd.read_csv(fp)
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"], utc=True)
    df = df.set_index("utc_timestamp")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df

# Plot summed actual vs forecast load over time
def plot_opsd_total_load_over_time(
    fp: str | Path,
    start_time: str | None = None,
    end_time: str | None = None,
    max_points: int = 500,
):
    """
    Plot total actual vs forecast load across all countries in OPSD dataset.
    """
    df = _read_opsd_60min_csv(fp)

    if start_time:
        df = df[df.index >= pd.to_datetime(start_time).tz_localize("UTC")]
    if end_time:
        df = df[df.index <= pd.to_datetime(end_time).tz_localize("UTC")]
 
    actual_cols = [c for c in df.columns if c.endswith("_load_actual_entsoe_transparency")]
    forecast_cols = [c for c in df.columns if c.endswith("_load_forecast_entsoe_transparency")]

    df["total_actual"] = df[actual_cols].sum(axis=1)
    df["total_forecast"] = df[forecast_cols].sum(axis=1)

    if len(df) > max_points:
        step = max(1, len(df) // max_points)
        df = df.iloc[::step]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["total_actual"], label="Total Load – Actual", color="tab:blue")
    plt.plot(df.index, df["total_forecast"], label="Total Load – Forecast", color="tab:orange")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Power (W)")
    plt.title(f"Total Load Over Time\n{start_time or 'Start'} → {end_time or 'End'}")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

# Plot max output for solar, wind onshore, wind offshore
def plot_opsd_max_energy_by_category(
    fp: str | Path,
    start_time: str | None = None,
    end_time: str | None = None,
    max_points: int = 500,
):
    """
    Plot max power generation for Solar, Wind Onshore, Wind Offshore in OPSD.
    """
    df = _read_opsd_60min_csv(fp)

    if start_time:
        df = df[df.index >= pd.to_datetime(start_time).tz_localize("UTC")]
    if end_time:
        df = df[df.index <= pd.to_datetime(end_time).tz_localize("UTC")]

    if len(df) > max_points:
        step = max(1, len(df) // max_points)
        df = df.iloc[::step]

    category_map = {
        "solar": [c for c in df.columns if "_solar_generation_actual" in c],
        "wind_onshore": [c for c in df.columns if "_wind_onshore_generation_actual" in c],
        "wind_offshore": [c for c in df.columns if (
            "_wind_offshore_generation_actual" in c or 
            ("_wind_generation_actual" in c and "_offshore" in c))
        ]
    }

    max_by_type = {}
    for label, cols in category_map.items():
        if not cols:
            print(f"[!] No data found for {label}")
            continue
        max_val = df[cols].sum(axis=1).max()
        max_by_type[label.replace("_", " ").title()] = round(max_val, 3)

    if not max_by_type:
        raise ValueError("No renewable energy types found in dataset.")

    # Plot
    plt.figure(figsize=(10, 6))
    ax = pd.Series(max_by_type).sort_values(ascending=False).plot(
        kind='bar', color='skyblue', edgecolor='black'
    )
    
    plt.ylabel("Max Power (W)")
    plt.title(f"Maximum Renewable Output by Type\n{start_time or 'Start'} → {end_time or 'End'}")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height} W",
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()


def plot_opsd_daily_avg_renewables(
    fp: str | Path,
    start_time: str | None = None,
    end_time: str | None = None
):
    """
    Plot the **yearly average of daily average renewable output** for each renewable profile.
    Categories include solar, wind onshore, and wind offshore (if available).
    """
    df = _read_opsd_60min_csv(fp)

    if start_time:
        df = df[df.index >= pd.to_datetime(start_time).tz_localize("UTC")]
    if end_time:
        df = df[df.index <= pd.to_datetime(end_time).tz_localize("UTC")]

    # Identify all renewable columns
    renewable_cols = [c for c in df.columns if any(sub in c for sub in [
        "_solar_generation_actual",
        "_wind_onshore_generation_actual",
        "_wind_offshore_generation_actual",
        "_wind_generation_actual"
    ])]

    if not renewable_cols:
        raise ValueError("No renewable energy profiles found.")

    # Compute daily averages
    df_daily_avg = df[renewable_cols].resample("1D").mean()

    # Compute yearly average of the daily averages for each column
    yearly_avg_per_profile = df_daily_avg.mean().sort_values(ascending=False)

    # Plot
    plt.figure(figsize=(24, 6))
    ax = yearly_avg_per_profile.plot(kind="bar", color="mediumseagreen", edgecolor="black")
    plt.ylabel("Yearly Avg Daily Generation (W)")
    plt.title("Yearly Average of Daily Renewable Output per Profile")
    plt.xticks(rotation=90, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Annotate bars with values
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:.0f} W",
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.show()