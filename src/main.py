from config import Config
import pandas as pd
from moduls.pipeline_de import preproc_pipe
from parallel_pandas import ParallelPandas

if __name__ == '__main__':
    cfg = Config()
    
    df = pd.read_csv(cfg.get_data_path())
    
    ParallelPandas.initialize(n_cpu=12, disable_pr_bar=False)

    df["feature_vec"] = df[cfg.txt_label].p_apply(preproc_pipe)
    df.dropna(inplace=True)
    
    df.drop(cfg.txt_label, axis=1).to_csv(cfg.get_data_out_path(), index=False)
    
    
    
    
    