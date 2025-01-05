__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os
import loguru

async def process_vector(data, collection_name):
    """
    Processes document chunks into a vector store.
    Args:
        data: Parsed document data.
        collection_name (str): Name of the vector store collection.
    Returns:
        Chroma: Initialized vector store.
    """
    try:
        embeddings = OllamaEmbeddings(
            model=os.getenv("APP_MODEL"),
            base_url="http://ollama:11434"  # Explicite le nom du service
        )
        
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        chunks = text_splitter.split_documents(data)
        
        db = Chroma.from_documents(
            collection_name=collection_name,
            documents=chunks,
            embedding=embeddings,
            persist_directory=os.getenv("DB_NAME")
        )
        
        return db
        
    except Exception as e:
        loguru.logger.exception("Full traceback:")
        raise e