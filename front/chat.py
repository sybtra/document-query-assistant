import requests
import os

def chat_with_collection(message, history, collection_name):
    """
    Function adapted for gr.ChatInterface that interacts with FastAPI.
    Args:
        message (str): The user's current message.
        history (list): The chat history [(user_message, bot_message), ...].
        collection_name (str): The name of the collection to use.
    Returns:
        str: Formatted response from the FastAPI endpoint or error message.
    """
    url = f"{os.getenv('API_URL')}/chat/{collection_name}"
    try:
        response = requests.post(url, json={"query": message, "history": history})
        if response.status_code == 200:
            cleaned_response = response.text.strip('"').replace('\\n', ' ')
            return cleaned_response
        else:
            return f"Error: {response.json()}"
    except Exception as e:
        return f"Connection error: {str(e)}"