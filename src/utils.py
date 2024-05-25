import pandas as pd
import os
from pathlib import Path

# absolute file path
abs_path = Path(os.path.abspath(__file__))


def read_data():
    df_us = read_data_us()
    df_ch = read_data_ch()
    df_eu = read_data_eu()
    
    return pd.concat([df_us, df_ch, df_eu], ignore_index=True) 

def read_data_us():
    data_folder = str(abs_path / '../input_data/us_ca')
    data_path1 = str(Path(data_folder) / 'trefferliste_2022.xls')
    data_path2 = str(Path(data_folder) / 'trefferliste_2023.xls')
    data_path3 = str(Path(data_folder) / 'trefferliste_2024.xls')
    
    df1 = read_data(data_path1)
    df2 = read_data(data_path2)
    df3 = read_data(data_path3)
    
    df = pd.concat([df1, df2, df3], ignore_index=True)
    
    df['origin'] = 'america'
    
    # concatenate the dataframes
    return df

def read_data_ch():
    data_folder = str(abs_path / '../input_data/ch')
    data_path1 = str(Path(data_folder) / '2022.xls')
    data_path2 = str(Path(data_folder) / '2023.xls')
    data_path3 = str(Path(data_folder) / '2024.xls')
    
    df1 = read_data(data_path1)
    df2 = read_data(data_path2)
    df3 = read_data(data_path3)
    
    df = pd.concat([df1, df2, df3], ignore_index=True)
    df['origin'] = 'asia'
    # concatenate the dataframes
    return df

def read_data_eu():
    data_folder = str(abs_path / '../input_data')
    data_path = str(Path(data_folder) / 'europe_data.xls')
    
    df = read_data(data_path)
    df['origin'] = 'eu'

    return df