# infrastructure/Retriever/fs_watcher.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DocsEventHandler(FileSystemEventHandler):
    def __init__(self, retriever):
        self.retriever = retriever

    def on_created(self, event):
        if event.src_path.lower().endswith(".pdf"):
            self._reindex()

    def on_deleted(self, event):
        if event.src_path.lower().endswith(".pdf"):
            self._reindex()

    def _reindex(self):
        print("⚡ Detectado cambio en docs: reindexando...")
        self.retriever.load_and_split()
        self.retriever.index()
        print("✅ Reindexacion completa.")

def start_watcher(retriever):
    """
    Arranca un Observer en background que vigila la carpeta retriever.docs_path.
    """
    event_handler = DocsEventHandler(retriever)
    observer = Observer()
    observer.schedule(event_handler, path=retriever.docs_path, recursive=False)
    observer.daemon = True
    observer.start()
    return observer
