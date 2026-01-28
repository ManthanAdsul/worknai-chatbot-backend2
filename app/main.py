from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.chat import router as chat_router
from app.routes.admin import router as admin_router
from app.models import StatusResponse

# ✅ FastAPI app MUST be at top-level
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered career mentor chatbot with RAG",
    version="1.0.0",
)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/", response_model=StatusResponse)
def root():
    return StatusResponse(
        status="success",
        message=f"{settings.APP_NAME} is running",
    )


@app.get("/health", response_model=StatusResponse)
def health():
    return StatusResponse(
        status="healthy",
        message="API is operational",
    )
