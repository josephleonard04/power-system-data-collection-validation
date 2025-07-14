import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def _read_consumption_csv(fp: str | Path) -> pd.DataFrame:
    """
    Load consumption CSV and parse timestamps with UTC.
    Assumes French CSVs with ';' separator and 'HORODATE' as datetime column.
    """
    df = pd.read_csv(fp, sep=";")
    df.rename(columns={"HORODATE": "time"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df


def plot_consumption_total_active_power(
    fp: str | Path,
    start_time: str | None = None,
    end_time: str | None = None,
    max_points: int = 500,
):
    """
    Plot the total active power (in MW) over time.
    """
    df = _read_consumption_csv(fp)

    if start_time:
        df = df[df["time"] >= pd.to_datetime(start_time, utc=True)]
    if end_time:
        df = df[df["time"] <= pd.to_datetime(end_time, utc=True)]

    # Sum energy consumption for all regions at each timestamp
    df_grouped = df.groupby("time")["ENERGIE_SOUTIREE"].sum().reset_index()

    # Convert from Wh/30min to kW
    df_grouped["total_active_power_mw"] = df_grouped["ENERGIE_SOUTIREE"] / 0.5 / 1000000000

    # Downsample if too many points
    if len(df_grouped) > max_points:
        step = max(1, len(df_grouped) // max_points)
        df_grouped = df_grouped.iloc[::step]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df_grouped["time"], df_grouped["total_active_power_mw"], label="Total Active Power (MW)", color="tab:blue")
    plt.xlabel("Time")
    plt.ylabel("Total Active Power (MW)")
    plt.title(f"Total Active Power Over Time\n{start_time or 'Start'} → {end_time or 'End'}")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
