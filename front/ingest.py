import requests
import os

def ingest_documents(collection_name, files):
    """
    Sends files to the FastAPI ingestion endpoint.
    Args:
        collection_name (str): The name of the collection to create or update.
        files (list): List of file objects to be ingested.
    Returns:
        str: Success message or error details.
    """
    url = f"{os.getenv('API_URL')}/ingest/{collection_name}"
    try:
        files_data = [('files', file) for file in files]
        response = requests.post(url, files=files_data)
        
        if response.status_code == 200:
            message = response.json().get('Message', 'No message returned.')
            return f"✅ **Ingestion successful**\n\n{message}"
        else:
            return f"❌ **Error**\n\n{response.json()}"
    except Exception as e:
        return f"❌ **Error during file upload**\n\n{str(e)}"