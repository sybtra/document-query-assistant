import magic
from langchain.document_loaders.parsers import BS4HTMLParser, PDFMinerParser
from langchain.document_loaders.parsers.txt import TextParser
from langchain.document_loaders.parsers.msword import MsWordParser
from langchain_community.document_loaders import Blob
from fastapi import UploadFile
import os
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

class OCRParser:
    """Parser to extract text from images via OCR"""
    def parse(self, blob: Blob):
        try:
            # Convert bytes to PIL image
            image = Image.open(io.BytesIO(blob.as_bytes()))
            # make OCR
            text = pytesseract.image_to_string(image)
            # Create a document with the extracted text
            from langchain.schema import Document
            return [Document(page_content=text, metadata={"source": "ocr"})]
        except Exception as e:
            raise Exception(f"Error in making OCR: {str(e)}")

class PDFOCRParser:
    """Parse for PDF with OCR if necessary"""
    def __init__(self):
        self.pdf_parser = PDFMinerParser()
        self.ocr_parser = OCRParser()

    def parse(self, blob: Blob):
        # Try normal parsing
        try:
            docs = self.pdf_parser.parse(blob)
            # If we get text, return the result
            if docs and any(doc.page_content.strip() for doc in docs):
                return docs
        except:
            pass

        # if no text or OCR Error
        try:
            # convert PDF to Image
            pdf_images = convert_from_bytes(blob.as_bytes())
            documents = []
            
            for i, image in enumerate(pdf_images):
                # Convert PIL image to bytes for OCR
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Create a new blob for the image
                image_blob = Blob.from_data(data=img_byte_arr, mime_type="image/png")
                
                # make OCR
                ocr_docs = self.ocr_parser.parse(image_blob)
                for doc in ocr_docs:
                    doc.page_content = i + 1
                documents.extend(ocr_docs)
            
            return documents
        except Exception as e:
            raise Exception(f"Error while PDF OCR: {str(e)}")

async def get_mime_type(filename: str, content: bytes) -> str:
    """
    Determine the MIME type of a file using the extension and content.
    """
    # Known MIME types by extension        
    MIME_TYPES = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.tiff': 'image/tiff',
        '.bmp': 'image/bmp'
    }
   
    # Verify extension
    ext = os.path.splitext(filename.lower())[1]
    if ext in MIME_TYPES:
        return MIME_TYPES[ext]
    # If not found by extension, use python-magic
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(content)
   
    # If we obtain application/octet-stream, we fall back on the extension
    if mime_type == 'application/octet-stream' and ext in MIME_TYPES:
        return MIME_TYPES[ext]
       
    return mime_type

async def parse_data(file: UploadFile):
    """
    Parses an uploaded file using the appropriate MIME-type-based parser.
    Args:
        file (UploadFile): The file to parse.
    Returns:
        List: Parsed documents.
    Raises:
        Exception: If parsing fails.
    """
    HANDLERS = {
        "application/pdf": PDFOCRParser(),
        "text/plain": TextParser(),
        "text/html": BS4HTMLParser(),
        "application/msword": MsWordParser(),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": MsWordParser(),
        "application/json": TextParser(),
        "image/png": OCRParser(),
        "image/jpeg": OCRParser(),
        "image/tiff": OCRParser(),
        "image/bmp": OCRParser()
    }
    
    try:
        # Read file content
        content = await file.read()
       
        # Get MIME type with our improved function
        mime_type = await get_mime_type(file.filename, content)
       
        if mime_type not in HANDLERS:
            raise ValueError(f"Type de fichier non supporté: {mime_type}")
       
        # Create the blob with the bytes
        blob = Blob.from_data(
            data=content,
            mime_type=mime_type,
        )
       
        # Parse the document
        parser = HANDLERS[mime_type]
        documents = parser.parse(blob=blob)
        
        # Ajouter le nom du fichier source aux métadonnées
        for doc in documents:
            doc.metadata["source"] = file.filename
       
        return documents
       
    except Exception as e:
        raise Exception(f"Error parsing document: {str(e)}")    
    finally:
        # Reset file for later use
        await file.seek(0)
        # Close file
        await file.close()
