from fastapi import APIRouter, HTTPException
from app.models import ChatMessage, ChatResponse
from app.services.rag_service import RAGService
from app.services.memory_service import MemoryService
from app.services.language_detector import detect_language
from app.utils.prompts import get_prompt_template
import uuid

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        session_id = message.session_id or str(uuid.uuid4())

        # 🔥 Instantiate per-request (CRITICAL)
        rag_service = RAGService()
        memory_service = MemoryService()

        detected_lang = detect_language(message.message)

        context, sources = rag_service.retrieve_context(message.message)

        history = memory_service.format_history_for_prompt(session_id)

        prompt_template = get_prompt_template(detected_lang)
        prompt = prompt_template.format(
            context=context,
            history=history,
            question=message.message
        )

        ai_response = rag_service.generate_response(prompt)

        memory_service.add_message(session_id, "user", message.message)
        memory_service.add_message(session_id, "assistant", ai_response)
        memory_service.save_session(session_id)

        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            detected_language=detected_lang
        )

    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
