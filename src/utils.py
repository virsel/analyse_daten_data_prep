import pandas as pd
import os
from pathlib import Path

# absolute file path
abs_path = Path(os.path.abspath(__file__)).parent

def read_data_us():
    data_folder = str(abs_path / "../input_data/us")
    data_path = str(Path(data_folder) / "combinded_data.csv")
    df = pd.read_csv(data_path)

    df["origin"] = "america"

    # concatenate the dataframes
    return df


def read_data_ch():
    data_folder = str(abs_path / "../input_data/ch")
    data_path = str(Path(data_folder) / "combinded_data.csv")
    df = pd.read_csv(data_path)
    
    df["origin"] = "asia"
    # concatenate the dataframes
    return df


def read_data_eu():
    data_folder = str(abs_path / "../input_data/eu")
    data_path = str(Path(data_folder) / "combinded_data.csv")
    df = pd.read_csv(data_path)

    df["origin"] = "eu"

    return df


def get_data():
    df_us = read_data_us()
    df_ch = read_data_ch()
    df_eu = read_data_eu()

    return pd.concat([df_us, df_ch, df_eu], ignore_index=True)
