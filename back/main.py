from fastapi import FastAPI
from routes import chat, ingest

app = FastAPI(debug=True)

tags_metadata = [
    {
        "name": "Documents",
        "description": "Collections & Documents API",
    },
    {
        "name": "Chat",
        "description": "Chat API",
    },
]

app.openapi_tags = tags_metadata

app.include_router(ingest.router)

app.include_router(chat.router)