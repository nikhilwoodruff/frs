import pandas as pd
import numpy as np
from frs.table_utils import resolve


def impute_missing_council_tax():
    df = pd.read_csv(resolve("csv/household.csv"))
    CT = pd.read_csv(resolve("resources/council_tax_stats.csv"))

    def impute_CT(row):
        if row["council_tax"] > 0:
            return row["council_tax"]
        match = CT[(CT["region"] == "london") & (CT["band"] == "D")].iloc[0]
        return np.maximum((np.random.randn(1) * match["stddev"] + match["council_tax"])[0], 0)

    df["council_tax"] = df.apply(impute_CT, axis=1)
    df.to_csv(resolve("csv/household.csv"))
    print("Imputed council taxes successfully.")
