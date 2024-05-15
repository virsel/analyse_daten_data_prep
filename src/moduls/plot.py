import hvplot.pandas 
import pandas as pd
from bokeh.models import NumeralTickFormatter

def frequent_words(series):
    word_freq = pd.Series(" ".join(series).split()).value_counts()
    return word_freq[1:40].rename("Word frequency of most common words in comments").hvplot.bar(
        rot=45
    ).opts(width=700, height=400, yformatter=NumeralTickFormatter(format="0,0"))