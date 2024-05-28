from moduls.pipeline_en import txt_cleaning
from parallel_pandas import ParallelPandas
ParallelPandas.initialize(n_cpu=12, split_factor=12, disable_pr_bar=False)

def pipe_preproc(df):
    df['text_preproc1'] = df['text'].p_apply(txt_cleaning)
    return df.drop(columns='text')