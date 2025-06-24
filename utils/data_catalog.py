# utils/data_catalog.py

import pandas as pd
from IPython.display import Markdown

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
            "Number of Profiles": "130",
            "Profile Types": ["load", "consumption points", "energy consumption"],
            "Load": ["active", "aggregated", "residential"],
            "Renewable": [],
            "Environment": [],
            "Economy": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2020–2024",
            "Time Resolution": ["30min"],
            "Geographical": ["France"],
            "Folder": "AgenceORE_Consumption_lt36kVA/"
        },
        {
            "Source": "eCO2mix_France_GenerationBySource",
            "Description": "Real-time and historical electricity generation, consumption, forecast, and emissions data for France, disaggregated by energy source and technology.",
            "Number of Profiles": "36",
            "Profile Types": ["load", "production", "renewable", "forecast", "environment" ],
            "Load": ["consumption", "active", "national", "aggregated"],
            "Renewable": ["solar", "wind", "hydro", "bioenergy"],
            "Environment": ["co2 intensity"],
            "Economy": [],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2012-2022",
            "Time Resolution": ["15min"],
            "Geographical": ["France"],
            "Folder": "eCO2mix_France_GenerationBySource/"
        },
        {
            "Source": "OPSD",
            "Description": "Open Power System Data - EU-wide TSO-provided time series",
            "Number of Profiles": "220",
            "Profile Types": ["load", "renewable", "capacity", "price", "forecast"],
            "Load": ["active", "aggregated", "national", "historical"],
            "Renewable": ["solar", "wind"],
            "Environment": [],
            "Economy": ["price"],
            "Processed": True,
            "Synthetic": False,
            "Horizon": "2015-2020",
            "Time Resolution": ["15min", "30min", "60min"],
            "Geographical": ["EU", "United Kingdom", "Switzerland", "Norway", "Montenegro", "Serbia", "Ukraine"],
            "Folder": "OPSD_TimeSeries/"
        },
        {
            "Source": "SimBench",
            "Description": "Synthetic power system benchmark datasets for grid studies",
            "Number of Profiles": 614,
            "Profile Types": ["load", "renewable", "powerplant", "storage"],
            "Load": ["active", "reactive", "residential", "industry", "commercial"],
            "Renewable": ["solar", "wind", "biomass", "hydro"],
            "Environment": [],
            "Economy": [],
            "Processed": True,
            "Synthetic": True,
            "Horizon": "2016-2017",
            "Time Resolution": ["15min"],
            "Geographical": ["Germany"],
            "Folder": "SimBench/"
        }
    ]
    df = pd.DataFrame(data_sources)
    pd.set_option('display.max_colwidth', None)
    return df

def query_data_sources(df, 
                       load=None, 
                       renewable=None, 
                       environment=None, 
                       economy=None,
                       synthetic=None,
                       processed=None,
                       geographical=None):
    
    result = df.copy()

    if load:
        result = result[result["Load"].apply(lambda x: all(item in x for item in load))]

    if renewable:
        result = result[result["Renewable"].apply(lambda x: all(item in x for item in renewable))]

    if environment:
        result = result[result["Environment"].apply(lambda x: all(item in x for item in environment))]

    if economy:
        result = result[result["Economy"].apply(lambda x: all(item in x for item in economy))]

    if synthetic is not None:
        result = result[result["Synthetic"] == synthetic]

    if processed is not None:
        result = result[result["Processed"] == processed]

    if geographical:
        if isinstance(geographical, str):
            geographical = [geographical]

        def geo_match(source_geo):
            expanded = []
            for g in source_geo:
                if g == "EU":
                    expanded.extend(EU_COUNTRIES)
                else:
                    expanded.append(g)
            return all(g in expanded for g in geographical)

        result = result[result["Geographical"].apply(geo_match)]

    return result.reset_index(drop=True)

def show_folder_links(results):
    if results.empty:
        return Markdown("**No datasets match your query.**")
    
    links = [f"- [{row['Source']}]({row['Folder']})" for _, row in results.iterrows()]
    return Markdown("\n".join(links))
