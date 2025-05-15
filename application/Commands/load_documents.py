from infrastructure.VectorStore.pdf_loader_Service import PDFVectorStoreService

def cargar_y_vectorizar_docs():
    pdf_service = PDFVectorStoreService(docs_path="docs")  # tu carpeta de PDFs
    pdf_service.index_all_pdfs()