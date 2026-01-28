from spacex_landing.wrangle import fill_payload_mass_with_mean
import pandas as pd
import numpy as np

def test_fill_payload_mass():
    df = pd.DataFrame({"PayloadMass":[1.0, np.nan, 3.0]})
    out = fill_payload_mass_with_mean(df)
    assert out["PayloadMass"].isna().sum() == 0
