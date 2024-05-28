from sentence_transformers import SentenceTransformer
from pathlib import Path
from umap import UMAP
import pandas as pd
import os

# absolute file path
abs_path = Path(os.path.abspath(__file__)).parent
data_path = str(abs_path / '../output/data_corpus.csv')
dataemb_out_path = str(abs_path / '../output/dataemb_corpus.csv')

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

umap_model = UMAP(n_neighbors=20, n_components=5, random_state=42)
# Further reduce the 5D embeddings to 2D
umap_model_2d = UMAP(n_components=2, n_neighbors=15, random_state=42, metric="cosine", verbose=True)

def pipe_emb(df):
    texts = df['text_preproc1'].tolist()
    # Start the multi-process pool on all available CUDA devices
    pool = model.start_multi_process_pool()
    # Compute the embeddings using the multi-process pool
    emb = model.encode_multi_process(texts, pool)
    print("Embeddings computed. Shape:", emb.shape)
    df['emb'] = emb.tolist()
    emb_reduced = umap_model.fit_transform(emb)
    df['emb_reduced'] = emb_reduced.tolist()
    emb_reduced_2d = umap_model.fit_transform(emb_reduced)
    df['emb_reduced_2d'] = emb_reduced_2d.tolist()

    return df[['id', 'emb', 'emb_reduced', 'emb_reduced_2d']]

if "__name__" == "__main__":
    df = pd.read_csv(data_path)
    df = pipe_emb(df)
    print(f"saving columns {df.columns} to {dataemb_out_path}")
    df.to_csv(dataemb_out_path, index=False)
