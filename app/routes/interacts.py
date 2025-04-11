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

import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

# Define the router
router = APIRouter()

# Load data from a JSON file
# with open("data.json", "r") as file:
#     data = json.load(file)
data = {
    "material_list": [
        {
            "material_id": "1",
            "material_title": "Material 1",
            "chapters": [
                {
                    "chapter_id": "1",
                    "chapter_title": "Chapter 1: Introduction",
                    "content": {
                        "text": "This is the content of Chapter 1.",
                        "images": [
                            {
                                "url": "https://example.com/images/example1.png",
                                "description": "Example image 1"
                            }
                        ]
                    }
                },
                {
                    "chapter_id": "2",
                    "chapter_title": "Chapter 2: Advanced Topics",
                    "content": {
                        "text": "This is the content of Chapter 2.",
                        "images": [
                            {
                                "url": "https://example.com/images/example2.png",
                                "description": "Example image 2"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "material_id": "2",
            "material_title": "Material 2",
            "chapters": [
                {
                    "chapter_id": "1",
                    "chapter_title": "Chapter 1: Basics",
                    "content": {
                        "text": "This is the content of Material 2, Chapter 1.",
                        "images": []
                    }
                }
            ]
        }
    ]
}

# Request body model
class CurrentContext(BaseModel):
    active_material_id: Optional[str] = None
    active_chapter_id: Optional[str] = None

class InteractRequest(BaseModel):
    user_text: str
    current_context: CurrentContext

# Response body models
class SpeakResponse(BaseModel):
    action_type: str = "SPEAK"
    data: Dict[str, str]

class PauseResponse(BaseModel):
    action_type: str = "PAUSE"
    data: Dict[str, str]

class PDFConvertResponse(BaseModel):
    action_type: str = "PDF_CONVERT"
    data: Dict[str, str]

class DisplayListResponse(BaseModel):
    action_type: str = "DISPLAY_LIST"
    data: Dict[str, List[Dict[str, str]]]

class DisplayContentResponse(BaseModel):
    action_type: str = "DISPLAY_CONTENT"
    data: Dict[str, Dict[str, str]]

class DisplayChapterResponse(BaseModel):
    action_type: str = "DISPLAY_CHAPTER"
    data: Dict[str, List[Dict[str, str]]]

class ErrorResponse(BaseModel):
    action_type: str = "ERROR"
    data: Dict[str, str]

# Route implementation
@router.post("/interact", response_model=Dict)
async def interact(request: InteractRequest):
    try:
        user_text = request.user_text.lower()
        current_context = request.current_context

        # Process the input and determine intent
        if "show list" in user_text:
            # Return the list of materials
            material_list = [{"id": material["material_id"], "title": material["material_title"]} for material in data["material_list"]]
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

        elif "chapter" in user_text and current_context.active_material_id:
            # Find the selected material and return its chapters
            material = next((m for m in data["material_list"] if m["material_id"] == current_context.active_material_id), None)
            if material:
                chapters = [{"id": chapter["chapter_id"], "title": chapter["chapter_title"]} for chapter in material["chapters"]]
                return DisplayChapterResponse(
                    data={"chapters": chapters}
                ).model_dump()
            else:
                return ErrorResponse(
                    data={"error_message": "Maaf, materi yang Anda cari tidak ditemukan."}
                ).model_dump()

        elif "content" in user_text and current_context.active_chapter_id:
            # Find the selected material and chapter, then return its content
            material = next((m for m in data["material_list"] if m["material_id"] == current_context.active_material_id), None)
            if material:
                chapter = next((c for c in material["chapters"] if c["chapter_id"] == current_context.active_chapter_id), None)
                if chapter:
                    return DisplayContentResponse(
                        data={
                            "material": {
                                "id": current_context.active_material_id,
                                "title": chapter["chapter_title"],
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
            return ErrorResponse(
                data={"error_message": "Maaf, saya tidak memahami apa yang Anda katakan."}
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