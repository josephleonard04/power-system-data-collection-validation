# utils/data_catalog.py

import pandas as pd
from IPython.display import HTML

EU_COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
    "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden"
]

def load_data_sources():
    data_sources = [
        {
            "Source": "AgenceORE_Consumption_lt36kVA",
            "Description": "Aggregated half-hourly electricity consumption data from consumption points with power subscriptions below 36kVA.",
            "Total Number of Profiles": "130",
            "Profile Types": ["load", "consumption points", "energy consumption"],
            "Type of Load": ["active", "aggregated", "residential"],
            "Renewable": [],
            "Environment": [],
            "Economy": [],
            "Voltage Level": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2020–2024",
            "Time Resolution": ["30min"],
            "Location": ["France"],
            "Geographical": ["regional", "distribution"],
            "Folder": "AgenceORE_Consumption_lt36kVA/"
        },
        {
            "Source": "eCO2mix_France_GenerationBySource",
            "Description": "Real-time and historical electricity generation, consumption, forecast, and emissions data for France, disaggregated by energy source and technology.",
            "Total Number of Profiles": "36",
            "Profile Types": ["load", "production", "renewable", "forecast", "environment"],
            "Type of Load": ["consumption", "active", "aggregated"],
            "Renewable": ["solar", "wind", "hydro", "bioenergy"],
            "Environment": ["co2 intensity"],
            "Economy": [],
            "Voltage Level": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2012-2022",
            "Time Resolution": ["15min"],
            "Location": ["France"],
            "Geographical": ["regional"],
            "Folder": "eCO2mix_France_GenerationBySource/"
        },
        {
            "Source": "ELMAS",
            "Description": "One-year dataset of hourly electrical load profiles from 424 French industrial and tertiary sectors (2018)",
            "Total Number of Profiles": 18,
            "Profile Types": ["load"],
            "Type of Load": ["active", "industrial", "tertiary", "clustered"],
            "Renewable": [],
            "Environment": [],
            "Economy": [],
            "Voltage Level": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2018",
            "Time Resolution": ["60min"],
            "Location": ["France"],
            "Geographical": ["national"],
            "Folder": "ELMAS/"
        },
        {
            "Source": "Ember",
            "Description": "Monthly electricity generation, demand, and emissions data for European countries, including breakdowns by fuel type and generation source",
            "Total Number of Profiles": "Varies by country and fuel type",
            "Profile Types": ["load", "renewable", "production"],
            "Type of Load": ["active", "aggregated"],
            "Renewable": ["wind", "solar", "hydro", "bioenergy"],
            "Environment": ["CO2 emissions", "CO2 intensity"],
            "Economy": [],
            "Voltage Level": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2015–2025",
            "Time Resolution": ["monthly"],
            "Location": ["Europe"],
            "Geographical": ["national"],
            "Folder": "Ember/"
        },
        {
            "Source": "OPSD",
            "Description": "Open Power System Data - EU-wide TSO-provided time series",
            "Total Number of Profiles": "220",
            "Profile Types": ["load", "renewable", "capacity", "price", "forecast"],
            "Type of Load": ["active", "aggregated", "historical"],
            "Renewable": ["solar", "wind"],
            "Environment": [],
            "Economy": ["price"],
            "Voltage Level": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2015-2020",
            "Time Resolution": ["15min", "30min", "60min"],
            "Location": ["EU", "United Kingdom", "Switzerland", "Norway", "Montenegro", "Serbia", "Ukraine"],
            "Geographical": ["national"],
            "Folder": "OPSD_TimeSeries/"
        },
        {
            "Source": "SimBench",
            "Description": "Synthetic power system benchmark datasets for grid studies",
            "Total Number of Profiles": 614,
            "Profile Types": ["load", "renewable", "powerplant", "storage"],
            "Type of Load": ["active", "reactive", "residential", "industry", "commercial"],
            "Renewable": ["solar", "wind", "biomass", "hydro"],
            "Environment": [],
            "Economy": [],
            "Voltage Level": ["mixed"],
            "Processed": True,
            "Synthetic": True,
            "Horizon": "2016-2017",
            "Time Resolution": ["15min"],
            "Location": ["Germany"],
            "Geographical": ["nodal"],
            "Folder": "SimBench/"
        },
        {
            "Source": "Zenodo",
            "Description": "Electric load profiles of 50 small and medium-sized industrial plants in Germany, recorded in 15-minute intervals over one year",
            "Total Number of Profiles": "50",
            "Profile Types": ["load"],
            "Type of Load": ["active", "industrial"],
            "Renewable": [],
            "Environment": [],
            "Economy": [],
            "Voltage Level": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2016-2017",
            "Time Resolution": ["15min"],
            "Location": ["Germany"],
            "Geographical": ["regional"],
            "Folder": "Zenodo/"
        }
    ]
    df = pd.DataFrame(data_sources)

    # Make 'Folder' column clickable links
    df["Folder"] = df["Folder"].apply(lambda f: f'<a href="{f}">Open Folder</a>')

    pd.set_option('display.max_colwidth', None)
    return df

def query_data_sources(df, **filters):
    result = df.copy()

    for key, value in filters.items():
        if key not in df.columns:
            raise ValueError(f"'{key}' is not a valid column. Available columns: {list(df.columns)}")

        if isinstance(df[key].iloc[0], list):
            if isinstance(value, str):
                value = [value]

            def list_match(source_list):
                expanded = []
                for item in source_list:
                    if item == "EU":
                        expanded.extend(EU_COUNTRIES)
                    else:
                        expanded.append(item)
                return all(v in expanded for v in value)

            result = result[result[key].apply(list_match)]
        else:
            result = result[result[key] == value]

    return result.reset_index(drop=True)

def show_data_table(results):
    if results.empty:
        return HTML("<b>No datasets match your query.</b>")

    # Render DataFrame as HTML with links
    return HTML(results.to_html(escape=False))
