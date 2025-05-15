# infrastructure/faq_service.py

from sklearn.cluster import DBSCAN
from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
from sqlalchemy import select , create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.user_repository import DATABASE_URL  # o tu módulo de configuración
from domain.message import Message # tu modelo ORM que tiene atributo .question
import numpy as np

class FAQService:
    def __init__(self, db_url: str):
        self.Session = sessionmaker(bind=create_engine(db_url))
        # Lo usamos sin carpeta de PDFs; simplemente pondremos los textos manualmente:
        self.retriever = TfidfRetriever(docs_path="", index_path=None)
    
    def top_n_faqs(self, n: int = 10, eps: float = 0.3):
        # 1) sacar todas las preguntas de la DB
        session = self.Session()
        try:
            questions = session.execute(select(Message.content)).scalars().all()
        finally:
            session.close()

        if not questions:
            return []

        # 2) inyectarlas y reindexar
        self.retriever.texts = questions
        # fuerza un nuevo fit
        X = self.retriever.vectorizer.fit_transform(questions)
        self.retriever.nn.fit(X)

        # 3) clustering DBSCAN con métrica coseno
        #    los eps más bajos => grupos más estrictos
        clustering = DBSCAN(
            metric="cosine",
            eps=eps,
            min_samples=1  # cada punto es al menos su propio cluster
        ).fit(X.toarray())

        labels = clustering.labels_

        # 4) contar y elegir un representante por cluster
        counts = {}
        reprs  = {}
        for lbl, q in zip(labels, questions):
            counts[lbl] = counts.get(lbl, 0) + 1
            # guarda siempre la primera pregunta vista en este cluster
            reprs.setdefault(lbl, q)

        # 5) ordena y toma top-N
        top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
        return [{"question": reprs[lbl], "count": cnt} for lbl, cnt in top]
