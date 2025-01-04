from fastapi import APIRouter, HTTPException, Depends, Body
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain
from config import Config, get_config

router = APIRouter()

@router.post("/chat/{collection_name}", tags=["Chat"])
async def process_chat(
    collection_name: str,
    query: str = Body(..., embed=True),
    config: Config = Depends(get_config),
):
    """
    POST Endpoint to process chat.

    Args:
        collection_name (str): Name of the collection to query.
        query (str): User's question or query.
        config (Config): Application configuration dependency.

    Returns:
        str: Response from the LLM model.

    Raises:
        HTTPException: In case of server errors.
    """
    try:
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=OllamaEmbeddings(model=config.APP_MODEL),
            persist_directory=config.DB_NAME
        )
        retriever = vector_store.as_retriever()
        conversation_chain = ConversationalRetrievalChain.from_llm(llm=config.llm, retriever=retriever, memory=memory)
        response = conversation_chain.invoke({"question": query})

        return response["answer"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e