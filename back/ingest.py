from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List

from utils.app_langchain.data_parser import parse_data
from utils.app_langchain.process_vector import process_vector
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

router = APIRouter()

@router.post("/ingest/{collection_name}", tags=["Documents"])
async def process_ingest(
    collection_name: str,
    files: List[UploadFile] = File(...),
):
    """
    POST Endpoint to ingest multiple files.

    Args:
        collection_name (str): Name of the collection to create or update.
        files (List[UploadFile]): List of files to be ingested.

    Returns:
        dict: Success message with file count.

    Raises:
        HTTPException: In case of ingestion or server errors.
    """
    try:
        embeddings = OllamaEmbeddings(model=os.getenv("APP_MODEL"))

        # Remove existing collection if it exists
        if os.path.exists(os.getenv("DB_NAME")):
            Chroma(
                persist_directory=os.getenv("DB_NAME"),
                embedding_function=embeddings,
                collection_name=collection_name
            ).delete_collection()

        # Process each file
        for file in files:
            parsed_data = await parse_data(file)
            await process_vector(parsed_data, collection_name=collection_name)

        return {"Message": f"Collection {collection_name} successfully created for {len(files)} files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e