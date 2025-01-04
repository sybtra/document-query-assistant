
# ChatBot Project with Frontend, Backend, and OCR Functionality

## Overview
This project is a ChatBot application that integrates a FastAPI backend, a Gradio-based frontend, and OCR capabilities using Tesseract for document processing. The backend leverages LangChain and Ollama for conversational AI, while the frontend offers a user-friendly interface.

## Features
- **Frontend**: Built with Gradio, providing a clean and interactive interface for document ingestion and chat functionality.
- **Backend**: Developed with FastAPI to handle document ingestion, chat processing, and OCR capabilities.
- **OCR Integration**: Tesseract OCR integrated into the backend for text extraction from images and PDFs.
- **LLM Integration**: Powered by the Llama 3.2 model via Ollama.

## Project Structure
```
.
├── front/
│   ├── interface.py
│   ├── requirements.txt
├── back/
│   ├── utils/
│   ├── config.py
├── docker-compose.yml
```

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.
- Python 3.9+ installed locally for development purposes (optional).

### Installation Steps

#### 1. Clone the Repository
```bash
git clone git@github.com:sybtra/document-query-assistant.git
cd document-query-assistant
```

#### 2. Build and Run Containers
Run the following command to build and start all services:
```bash
docker-compose up --build
```

This will:
- Launch the frontend on port `7860`.
- Launch the backend on port `8000`.
- Launch the Ollama service for the Llama 3.2 model on port `11434`.

#### 3. Access the Application
- Frontend: [http://localhost:7860](http://localhost:7860)
- Backend API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Backend Details

### OCR Capability
The backend uses Tesseract OCR for:
- Extracting text from images (PNG, JPEG, BMP, etc.).
- Extracting text from PDF documents when standard parsing fails.

### API Endpoints
1. **Document Ingestion**:
   - Endpoint: `POST /ingest/{collection_name}`
   - Description: Upload files to create or update a document collection.
   - Supported File Types: PDF, DOC, DOCX, TXT, HTML, PNG, JPEG, etc.

2. **Chat Processing**:
   - Endpoint: `POST /chat/{collection_name}`
   - Description: Process user queries against an ingested collection.

## Adding New Models or Capabilities
To integrate additional models or extend functionality, modify the `config.py` file and update the relevant services in `docker-compose.yml`.

## Development Notes

### Backend Requirements
Ensure the following dependencies are listed in `back/requirements.txt`:
```text
fastapi
langchain
langchain_chroma
langchain_ollama
pytesseract
pdf2image
Pillow
python-magic
```

### Frontend Requirements
Ensure the following dependencies are listed in `front/requirements.txt`:
```text
gr
requests
```

### Troubleshooting
- **Tesseract OCR Missing**:
  Ensure Tesseract is installed in the backend container by verifying the `Dockerfile.backend` includes:
  ```Dockerfile
  RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev && rm -rf /var/lib/apt/lists/*
  ```

- **Service Ports Not Available**:
  Ensure no other processes are using the specified ports (7860, 8000, 11434).

## License
This project is licensed under the MIT License.
