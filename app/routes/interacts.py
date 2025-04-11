"""
TODO:
Create a route to handle the interaction with the Voice assistant.

Receives raw text (from Android STT), processes it to understand intent, and returns instructions to the Android app.

# Route: /interact
# Method: POST
# Request Body: JSON object containing the user's input
example:
```json
{
  "user_text": "string", // Raw text from Android STT
  "current_context": {
    "active_material_id": "string | null" // ID of the currently active material in Android, or null
  }
}

# Response Body: JSON object
example:
{
  "action_type": "SPEAK" | "NAVIGATE" | "DISPLAY_LIST" | "DISPLAY_CONTENT" | "ERROR", // Type of action
  "data": { // Content varies based on action_type
    for SPEAK: "text_to_speak": "Text to be read aloud..."
    for NAVIGATE: "target_screen": "SCREEN_NAME (e.g., LIST_SCREEN)"
    for DISPLAY_LIST: "material_list": [ { "id": ..., "title": ... }, ... ]
    for DISPLAY_CONTENT: "material": { "id": ..., "title": ..., "content": ... }
    for ERROR/UNRECOGNIZE: "error_message": "Error message..."
  }
}
"""

from fastapi import APIRouter, HTTPException
from app.routes.models import (
    InteractRequest, SpeakResponse, PauseResponse, PDFConvertResponse,
    DisplayListResponse, DisplayContentResponse, DisplayChapterResponse, ErrorResponse
)
from app.data.mock_data import materials_mockup
from typing import Dict

# Define the router
router = APIRouter()

# Route implementation
@router.post("/interact", response_model=Dict)
async def interact(request: InteractRequest):
    try:
        user_text = request.user_text.lower()
        current_context = request.current_context

        # Process the input and determine intent
        if "show list" in user_text:
            # Return the list of materials
            material_list = [{"id": material["id"], "title": material["title"]} for material in materials_mockup]
            return DisplayListResponse(
                data={"material_list": material_list}
            ).model_dump()
        
        elif "speak" in user_text:
            # Respond with a speak action
            return SpeakResponse(
                data={"text_to_speak": "Baik, saya akan melanjutkan"}
            ).model_dump()

        elif "pause" in user_text:
            # Respond with a pause action
            return PauseResponse(
                data={"text_to_speak": "Baik, saya akan berhenti"}
            ).model_dump()

        elif "pdf" in user_text:
            # Respond with a PDF conversion action
            return PDFConvertResponse(
                data={"message": f"Baik terima kasih. Materi yang Anda unggah akan saya konversi ke PDF."}
            ).model_dump()

        elif "chapter" in user_text:
            # Find the selected material and return its chapters
            material = next((m for m in materials_mockup if m["id"] == current_context.active_material_id), None)
            if material and current_context.active_material_id:
                chapters = [{"id": chapter["id"], "title": chapter["title"]} for chapter in material["chapters"]]
                return DisplayChapterResponse(
                    data={"chapters": chapters}
                ).model_dump()
            else:
                return ErrorResponse(
                    data={"error_message": "Maaf, materi yang Anda cari tidak ditemukan."}
                ).model_dump()

        elif "content" in user_text:
            material = next((m for m in materials_mockup if m["id"] == current_context.active_material_id), None)
            if material and current_context.active_material_id:
                chapter = next((c for c in material["chapters"] if c["id"] == current_context.active_chapter_id), None)
                if chapter and current_context.active_chapter_id:
                    return DisplayContentResponse(
                        data={
                            "material": {
                                "id": current_context.active_chapter_id,
                                "title": chapter["title"],
                                "subtitle": chapter["subtitle"],
                                "content": chapter["content"]
                            }
                        }
                    ).model_dump()
                else:
                    return ErrorResponse(
                        data={"error_message": "Maaf, bab yang Anda cari tidak ditemukan."}
                    ).model_dump()
            else:
                return ErrorResponse(
                    data={"error_message": "Maaf, materi yang Anda cari tidak ditemukan."}
                ).model_dump()
            

        else:
            # Handle unrecognized commands
            return ErrorResponse(
                data={"error_message": "Maaf, saya tidak mengerti perintah Anda."}
            ).model_dump()

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    
"""
Example of how to use the router in Postman
POST http://127.0.0.1:8000/api/interact
Body:
{
  "user_text": "content",
  "current_context": {
    "active_material_id": "1",
    "active_chapter_id": "1"
  }
}
Try different user_text values to test different responses.
- "speak"
- "navigate"
- "show list"
- "chapter" 
"""