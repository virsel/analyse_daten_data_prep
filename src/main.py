from config import Config
import pandas as pd
from _2_preproc_pipeline_en.main import pipe_preproc as pipe_preproc_en
from _2_preproc_pipeline_de.main import pipe_preproc as pipe_preproc_de
from utils import get_data
from _1_data_prepared_input.utils import pipe_arrangement
from pathlib import Path
import os

# absolute file path
abs_path = Path(os.path.abspath(__file__)).parent
data_out_path = str(abs_path / '../output/data_corpus.csv')

if __name__ == '__main__':
    cfg = Config()
    
    df = get_data()
    
    df = pipe_arrangement(df)
    
    df_en = df[df.lang == 'en'].copy()
    df_de = df[df.lang == 'de'].copy()
    df_en = pipe_preproc_en(df_en)
    df_de = pipe_preproc_de(df_de)
    df = pd.concat([df_en, df_de])
    
    df.to_csv(data_out_path, index=False)
    
    
    
    
    
    
    