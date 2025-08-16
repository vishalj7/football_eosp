from data import api_call
from func import eosp_functions
import pandas as pd
from io import StringIO


elo_data = api_call.make_api_call("2025-01-01")
elo_data = StringIO(elo_data)
elo_df = pd.read_csv(elo_data, sep=",")

print(elo_df.head(10))
