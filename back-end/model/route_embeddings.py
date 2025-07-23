from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

class RouteEmbeddings:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.df['route_text'] = self.df.apply(
            lambda row: f"{row['RouteStart']} até {row['RouteEnd']}", axis=1
        )

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = self.model.encode(self.df['route_text'].tolist(), show_progress_bar=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype('float32'))

    def search(self, origin_text, destination_text, top_k=1):
        """ Busca as rotas mais similares e retorna o resultado e as distâncias (confiança) """
        query = f"{origin_text} até {destination_text}"
        query_embedding = self.model.encode([query])[0].astype('float32')

        distances, indices = self.index.search(np.array([query_embedding]), top_k)

        results = self.df.iloc[indices[0]]
        return results.reset_index(drop=True), distances[0]