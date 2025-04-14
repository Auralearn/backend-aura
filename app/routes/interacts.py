from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional

from app.schemas.base import StandardResponse
from app.schemas.interacts import InteractRequest, BaseActionResponse
from app.schemas.materials import Material

from app.utils.exceptions import NotFoundError, BadRequestError, ServerError

from app.services.gemini_service import gemini_genetare_content, construct_educational_voice_prompt

from app.data.mock_data import materials_mockup

# Define the router
router = APIRouter()

# Query category for interact
interact_query_category = {
    "speak": ["apa", "mengapa", "siapa", "dimana", "kapan", "bagaimana", "tolong jelaskan", "apa itu", "apa yang dimaksud", "apa yang dimaksud dengan"],
    "action_material": ["buka materi", "buka buku", "lihat materi", "lihat buku", "tampilkan materi", "tampilkan buku"],
    "pdf": ["buka pdf scan", "buka scan pdf", "buka pdf", "pdf"]
}

def load_materials() -> List[Material]:
    """
    TODO: Ganti ini dengan load dari database setelah test
    """
    result: List[Material] = []
    for material in materials_mockup:
        result.append(Material(**material))
    return result

# Route implementation
@router.post(
    "/interact", 
    response_model=StandardResponse[BaseActionResponse],
    summary="Process voice command",
    description="Process the voice command and return the appropriate action response"
)
async def interact(request: InteractRequest):
    """
    Process user voice commands and return appropriate actions
    
    This endpoint handles different types of voice commands like asking questions,
    navigating materials, and more.
    """
    def model_answer(question: str, context: str) -> str:
        """Generate an answer to a user question (placeholder for AI model)"""
        return f"This is the model answer to your question: '{question}'"
    
    try:
        user_text = request.user_text.lower()
        current_context = request.current_context

        # Process the input and determine intent
        if any(phrase in user_text for phrase in interact_query_category["speak"]):
            # Handle speak action
            return StandardResponse(
                success=True,
                data=BaseActionResponse(
                    action_type="SPEAK",
                    text_audio=model_answer(user_text),
                    params=None
                )
            )
        
        elif any(phrase in user_text for phrase in interact_query_category["action_material"]):
            prompt = """Mana yang paling mirip untuk "{MATERIAL_TITLE}"?

untuk database judul:
{MATERIAL_TITLE_LIST}

berikan jawaban saja tanpa ada awalan akhiran lain
"""
            material_title = ""
            for phrase in interact_query_category["action_material"]:
                if phrase in user_text:
                    material_title = user_text.replace(phrase, "").strip()
                    break

            materials = load_materials()
            materials_title_id = [
                [material.title, material.id] for material in materials
            ]
            
            materials_title_data_text = "\n".join(
                [f"{material[0]}: {material[1]}" for material in materials_title_id]
            )
                     
            prompt = prompt.format(
                MATERIAL_TITLE=material_title,
                MATERIAL_TITLE_LIST=materials_title_data_text
            )
            
            # Call the AI model to get the answer
            answer = await gemini_genetare_content(query=prompt)
            
            if answer:
                # Find the material ID from the answer
                for material in materials:
                    if str(material.id) in answer:
                        return StandardResponse(
                            success=True,
                            data=BaseActionResponse(
                                action_type="NAVIGATE",
                                text_audio=f"Berikut adalah materi yang kamu cari: {material.title}",
                                params={
                                    "intent": "open_material",
                                    "material_id": material.id}
                            )
                        )
            else:
                return StandardResponse(
                    success=True,
                    data=BaseActionResponse(
                        action_type="SPEAK",
                        text_audio="Maaf saya tidak bisa menemukan materi yang kamu cari",
                        params=None
                    )
                )
                
        elif any(phrase in user_text for phrase in interact_query_category["pdf"]):
            return StandardResponse(
                success=True,
                data=BaseActionResponse(
                    action_type="NAVIGATE",
                    text_audio="Berikut adalah pdf scanner",
                    params={"intent": "open_pdf_scanner"}
                )
            )
        
        else:
            return StandardResponse(
                success=True,
                data=BaseActionResponse(
                    action_type="UNRECOGNIZED",
                    text_audio="Maaf saya tidak bisa memahami apa yang kamu maksud",
                    params=None
                )
            )

    except (BadRequestError, NotFoundError) as e:
        # These exceptions will be handled by the exception handlers
        raise e
    except Exception as e:
        # Convert unexpected exceptions to ServerError
        raise ServerError(detail=f"An unexpected error occurred: {str(e)}")