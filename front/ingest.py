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
            return f"Ingestion successful: {response.json().get('Message', 'No message returned.')}"
        else:
            return f"Error: {response.json()}"
    except Exception as e:
        return f"Error during file upload: {str(e)}"