# simbench_plotter.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Literal


def _read_simbench_csv(fp: str | Path) -> pd.DataFrame:
    """
    Read a SimBench CSV, normalize 'time' column, and parse European datetime format.
    """
    df = pd.read_csv(fp, sep=";")
    time_col = [col for col in df.columns if col.lower() == "time"]
    if not time_col:
        raise ValueError("No 'time' column found.")
    df.rename(columns={time_col[0]: "time"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"], dayfirst=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def plot_simbench_total_load_over_time(
    fp: str | Path,
    kind: Literal["pload", "qload"] = "pload",
    start_time: str | None = None,
    end_time: str | None = None,
    max_points: int = 500,
):
    """
    Plot the total (summed) load over time for active or reactive load.
    """
    df = _read_simbench_csv(fp)

    if start_time:
        df = df[df["time"] >= pd.to_datetime(start_time)]
    if end_time:
        df = df[df["time"] <= pd.to_datetime(end_time)]

    cols = [c for c in df.columns if c.endswith(f"_{kind}")]
    if not cols:
        raise ValueError(f"No '{kind}' columns found in file.")

    df["total"] = df[cols].sum(axis=1)

    if len(df) > max_points:
        step = max(1, len(df) // max_points)
        df = df.iloc[::step]

    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["total"], label=f"Total {kind.upper()}", color="tab:blue")
    label = "Active" if kind == "pload" else "Reactive"
    plt.xlabel("Time")
    plt.ylabel("Total Power (kW)")
    plt.title(f"Total {label} Load Over Time\n{start_time or 'Start'} → {end_time or 'End'}")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


def unnormalize_simbench_loadprofile(
    fp_profile: str | Path,
    fp_capacity: str | Path,
    output_fp: str | Path = "raw/consumer/LoadProfile_scaled.csv",
    plot: bool = True,
    default_capacity: float = 1.0
):
    """
    Unnormalize LoadProfile.csv using pLoad values from Load.csv and save the scaled version.
    Missing profiles will be scaled with default_capacity silently.
    Optionally plot the result using the bar chart function.
    """
    load_info = pd.read_csv(fp_capacity, sep=";")
    capacity_map = load_info.groupby("profile")["pLoad"].sum().to_dict()

    df = pd.read_csv(fp_profile, sep=";")
    cols = [col for col in df.columns if col.endswith("_pload")]

    for col in cols:
        profile = col.replace("_pload", "")
        capacity = capacity_map.get(profile, default_capacity)
        df[col] = df[col] * capacity

    df.to_csv(output_fp, sep=";", index=False)

    if plot:
        plot_simbench_profile_max_loads_as_bar(output_fp, kind="pload", figsize="auto")


def plot_simbench_profile_max_loads_as_bar(
    fp: str | Path,
    kind: Literal["pload", "qload"] = "pload",
    figsize: tuple | Literal["auto"] = "auto"
):
    """
    Bar plot of max load for each individual profile (active/reactive).
    Use figsize="auto" to dynamically scale width based on number of profiles.
    """
    df = _read_simbench_csv(fp)
    cols = [c for c in df.columns if c.endswith(f"_{kind}")]
    if not cols:
        raise ValueError(f"No '{kind}' columns found.")

    max_vals = df[cols].max().sort_values(ascending=False)

    # Auto-size width if specified
    if figsize == "auto":
        width = max(14, len(max_vals) * 0.4)  # 0.4 inch per profile
        figsize = (width, 6)

    plt.figure(figsize=figsize)
    ax = max_vals.plot(kind="bar", color="cornflowerblue", edgecolor="black")
    plt.ylabel("Max Load (W)")
    plt.title(f"Maximum {kind.upper()} Load per Profile")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_simbench_res_daily_avg_as_bar(fp: str | Path):
    """
    For each RES profile (PV, WP, BM, Hydro...), compute:
    - Daily average time series
    - Then take the **yearly mean** of daily averages
    - Plot the results as a bar chart
    """
    df = _read_simbench_csv(fp)
    df.set_index("time", inplace=True)

    # Get all renewable columns
    res_cols = [col for col in df.columns if col.startswith(("PV", "WP", "BM", "Hydro"))]
    if not res_cols:
        raise ValueError("No RES columns found.")

    # Step 1: Resample to daily averages
    df_daily_avg = df[res_cols].resample("1D").mean()

    # Step 2: Compute yearly average of the daily averages for each profile
    yearly_avg = df_daily_avg.mean().sort_values(ascending=False)

    # Step 3: Plot
    plt.figure(figsize=(16, 6))
    ax = yearly_avg.plot(kind="bar", color="mediumseagreen", edgecolor="black")

    plt.ylabel("Yearly Average of Daily Avg Output (normalized)")
    plt.title("Yearly Average Renewable Output per Profile (Daily Avg)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()