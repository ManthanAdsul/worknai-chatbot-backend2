from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models import StatusResponse
from app.services.rag_service import rag_service
import PyPDF2
import io

router = APIRouter()

@router.post("/admin/upload-pdf", response_model=StatusResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file to the knowledge base.
    """
    try:
        # Read PDF content
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)
        
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Add to vector store
        rag_service.add_documents(
            texts=[text],
            metadatas=[{"source": file.filename, "type": "pdf"}]
        )
        
        return StatusResponse(
            status="success",
            message=f"PDF '{file.filename}' uploaded and indexed successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/add-text", response_model=StatusResponse)
async def add_text(text: str, source: str = "manual"):
    """
    Add plain text to the knowledge base.
    """
    try:
        rag_service.add_documents(
            texts=[text],
            metadatas=[{"source": source, "type": "text"}]
        )
        
        return StatusResponse(
            status="success",
            message="Text added to knowledge base successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))