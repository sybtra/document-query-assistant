# Document Query Assistant

## Overview
This project is a document query assistant that combines a FastAPI backend with a Gradio frontend, featuring OCR capabilities. It uses LangChain and Ollama for document processing and conversational AI, with a focus on secure inter-service communication.

## Features
- **Document Processing**: Support for multiple file formats including PDF, DOCX, TXT, HTML with OCR capabilities
- **Interactive Chat**: Context-aware chatbot interface for querying document content
- **Secure Architecture**: Isolated service communication with Docker networks
- **OCR Integration**: Automated text extraction from images and scanned PDFs
- **LLM Integration**: Powered by Ollama with optimized RAG configuration

## Project Structure
```
.
├── front/
│   ├── interface.py          # Main Gradio application
│   ├── chat.py         # Chat functionality
│   ├── ingest.py       # Document ingestion
│   ├── Dockerfile
│   ├── requirements.txt
├── back/
│   ├── routes/
│   │   ├── chat.py     # Chat endpoints
│   │   ├── ingest.py   # Ingestion endpoints
│   ├── utils/
│   │   ├── app_langchain/
│   │   │   ├── data_parser.py
│   │   │   ├── process_vector.py
│   ├── config.py       # Application configuration
│   ├── Dockerfile
│   ├── requirements.txt
├── docker-compose.yml
├── .env.example
```

## Network Architecture
The application uses isolated Docker networks for security:
- `front-back`: Communication between frontend and backend
- `back-ollama`: Communication between backend and Ollama
- External access only to frontend (7860) and backend API (8000)

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/sybtra/document-query-assistant.git
cd document-query-assistant
```

2. **Configure Environment**
Create a `.env` file:
```env
API_URL=http://backend:8000
DB_NAME=/app/data/chroma
APP_MODEL=llama2
MODEL_BASE_URL=http://ollama:11434
```

3. **Build and Run**
```bash
docker compose up --build
```

### Accessing the Application
- Frontend Interface: http://localhost:7860
- API Documentation: http://localhost:8000/docs

## API Endpoints

### Document Ingestion
- **Endpoint**: `POST /ingest/{collection_name}`
- **Purpose**: Upload and process documents
- **Supported Formats**:
  - Text: `.txt`, `.json`
  - Documents: `.pdf`, `.docx`, `.doc`
  - Web: `.html`, `.htm`
  - Images (via OCR): `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`

### Chat Interface
- **Endpoint**: `POST /chat/{collection_name}`
- **Purpose**: Process queries against ingested documents
- **Features**: 
  - Context-aware responses
  - RAG-optimized configuration
  - Conversation memory

## Development

### Backend Requirements
```text
fastapi
uvicorn
python-multipart
langchain
langchain_community
langchain_core
langchain_chroma
langchain_ollama
pytesseract
pdf2image
python-magic
python-dotenv
loguru
```

### Frontend Requirements
```text
gradio
python-dotenv
requests
```

## Docker Configuration

### Services
1. **Frontend**
   - Port: 7860
   - Network: front-back
   - Dependencies: backend

2. **Backend**
   - Port: 8000
   - Networks: front-back, back-ollama
   - Volumes: chroma_data

3. **Ollama**
   - Internal Port: 11434
   - Network: back-ollama
   - Volumes: ollama_data

## Troubleshooting

### Common Issues
1. **Connection Refused**
   - Verify network configurations in docker-compose.yml
   - Check service health status
   - Ensure correct environment variables

2. **File Processing Errors**
   - Verify file format support
   - Check OCR configuration
   - Ensure sufficient permissions

### Maintenance
- Regular model updates via Ollama
- Vector store maintenance
- Log monitoring

## License
MIT License

## Repository
[https://github.com/sybtra/document-query-assistant.git](https://github.com/sybtra/document-query-assistant.git)