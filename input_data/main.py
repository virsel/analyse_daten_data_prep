import pandas as pd
import os
from pathlib import Path


abs_path = Path(os.path.abspath(__file__)).parent
data_folders = [str(abs_path / 'us'), str(abs_path / 'eu'), str(abs_path / 'ch')]

def read_data(path):
    df = pd.read_excel(
        path,
        header=1,
        usecols=[
            "Veröffentlichungs-Nummer",
            "Titel",
            "Zusammenfassung",
            "Veröffentlichungs-Datum",
            "IPC-Hauptklasse",
            "IPC-Neben-/Indexklassen",
        ],
    )

    return df

def concatenate_data(folder):
    # Get the list of all Excel files in the folder
    files = [f for f in os.listdir(folder) if f.endswith('.xls') or f.endswith('.xlsx')]
    
    # Read and concatenate all Excel files in the folder
    dataframes = [read_data(os.path.join(folder, file)) for file in files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    return combined_df

def merge_data():
    for folder in data_folders:
        combinded_df = concatenate_data(folder)
        # Save the concatenated DataFrame to a new Excel file (optional)
        combinded_df.to_csv(f'{folder}/combined_data.csv', index=False)


if __name__ == '__main__':
    merge_data()