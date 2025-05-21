# main.py
from fastapi import FastAPI
from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
from infrastructure.Retriever.fs_watcher import start_watcher
from application.Services.Chat_Service import ChatService
from Presentation.Routes.Chat_route import router as chat_router
from Presentation.Routes.user_route import router as user_router
from contextlib import asynccontextmanager

app = FastAPI()
app.include_router(chat_router)
app.include_router(user_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1) Inicializa tu retriever e indexa si es necesario
    retriever = TfidfRetriever(docs_path="docs")
    try:
        retriever.load_index()
    except FileNotFoundError:
        retriever.load_and_split()
        retriever.index()

    # 2) Crea tu ChatService
    chat_service = ChatService(retriever=retriever)

    # 3) Guarda en app.state para que los routers lo lean
    app.state.tfidf_retriever = retriever
    app.state.chat_service   = chat_service

    # 4) Arranca el watcher para reindexar al detectar cambios
    start_watcher(retriever)

    print("✅ Startup completo. Watcher activo en 'docs/'")


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del ChatBot"}

