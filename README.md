# Power System Data Collection and Validation
This project cleans and validates time series datasets related to electricity systems. It serves as a centralized resource to support analysis, planning, and simulation in energy network research. The datasets include synthetic and real-world measurements of load, generation, and market prices, structured to ensure clarity, consistency, and reproducibility.

---

## Project Structure
```plaintext
Power_System_Data_Collection_and_Validation/
├── OPSD_TimeSeries/
│   ├── cleaned/
│   ├── raw/
│   └── opsd_analysis.ipynb
│
├── SimBench/
│   ├── cleaned/
│   ├── raw/
│   └── simbench_analysis.ipynb
│
├── other sources etc. (It will be added in the future)
│
└── README.md
```


## Data Sources
| Source     | Description                                                                                         | Documentation                                                  | Repository                                      |
|------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------|--------------------------------------------------|
| **SimBench** | Benchmark grids with full-year time series data for load, generation, and storage. | [SimBench Docs](https://simbench.readthedocs.io/en/stable/) | [GitHub](https://github.com/e2nIEE/simbench) |
| **OPSD – Time Series** | Real-world electricity load, renewable generation, capacity, and day-ahead prices for 32 European countries (2015–2020). | [OPSD Docs](https://data.open-power-system-data.org/time_series/2020-10-06/) | [GitHub](https://github.com/Open-Power-System-Data/datapackage_timeseries) |

---



