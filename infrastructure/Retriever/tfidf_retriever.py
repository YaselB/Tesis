import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pickle

class TfidfRetriever:
    def __init__(self, docs_path: str, index_path: str = "tfidf_index.pkl"):
        self.docs_path = docs_path
        self.index_path = index_path
        self.vectorizer = TfidfVectorizer()
        self.nn = NearestNeighbors(n_neighbors=3 , metric="cosine")
        self.texts = []
        self.tfidf_matriz = None
    def load_and_split(self , chunk_size: int = 500):
        """Carga PDFs y los divide en fragmentos de chunk_size caracteres"""
        import fitz
        fragments = []
        for fname in os.listdir(self.docs_path):
            if not fname.lower().endswith(".pdf"):
                continue
            file_path = fitz.open(os.path.join(self.docs_path , fname))
            doc = fitz.open(file_path)
            fullText = "".join(page.get_text() for page in doc)
            # fragmentar por tamaño fijo
            for i in range(0 , len(fullText) , chunk_size):
                fragments.append(fullText[i:i+chunk_size])
            self.texts = fragments
    def index(self):
        """Generar TF-IDF , entrena el NearestNeighbors y guarda el índice."""
        self.tfidf_matriz = self.vectorizer.fit_transform(self.texts)
        self.nn.fit(self.tfidf_matriz)
        with open(self.index_path , "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "nn": self.nn,
                "texts": self.texts
            } , f)
    def load_index(self):
        """Cargar vectorizer , nearest neighbors y texts"""
        with open(self.index_path , "rb") as f:
            data = pickle.load(f)
        self.vectorizer = data["vectorizer"]
        self.nn = data["nn"]
        self.texts = data["texts"]
    def query(self , query: str):
        """Vectoriza la pregunta , busca los vecinos mas cercanos y devuelve los textos."""
        q_vec = self.vectorizer.transform([query])
        distances , idxs = self.nn.kneighbors(q_vec)
        return [(self.texts[idxs] , float(dist))
                for dist , idxs in zip(distances[0] , idxs[0])]