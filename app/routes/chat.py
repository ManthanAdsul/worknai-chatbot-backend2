from fastapi import APIRouter, HTTPException
from app.models import ChatMessage, ChatResponse
from app.services.rag_service import rag_service
from app.services.memory_service import memory_service
from app.services.language_detector import detect_language
from app.utils.prompts import get_prompt_template
import uuid

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Main chat endpoint that processes user messages and returns AI responses.
    """
    try:
        # Generate session ID if not provided
        session_id = message.session_id or str(uuid.uuid4())
        
        # Detect language
        detected_lang = detect_language(message.message)
        
        # Retrieve relevant context from vector store
        context, sources = rag_service.retrieve_context(message.message)
        
        # Get conversation history
        history = memory_service.format_history_for_prompt(session_id)
        
        # Build prompt
        prompt_template = get_prompt_template(detected_lang)
        prompt = prompt_template.format(
            context=context,
            history=history,
            question=message.message
        )
        
        # Generate response
        ai_response = rag_service.generate_response(prompt)
        
        # Save to memory
        memory_service.add_message(session_id, "user", message.message)
        memory_service.add_message(session_id, "assistant", ai_response)
        
        # Save session to file (for logging)
        memory_service.save_session(session_id)
        
        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            detected_language=detected_lang
        )
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))