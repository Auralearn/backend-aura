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
from pydantic import BaseModel
from typing import Optional, List, Dict

# Define the router
router = APIRouter()

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

class NavigateResponse(BaseModel):
    action_type: str = "NAVIGATE"
    data: Dict[str, str]

class DisplayListResponse(BaseModel):
    action_type: str = "DISPLAY_LIST"
    data: Dict[str, List[Dict[str, str]]]

class Content(BaseModel):
    text: str
    images: Optional[List[Dict[str, str]]] = None

class Material(BaseModel):
    id: str
    title: str
    content: Content

class DisplayContentResponse(BaseModel):
    action_type: str = "DISPLAY_CONTENT"
    data: Dict[str, Material]

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
        if "speak" in user_text:
            return SpeakResponse(
                data={"text_to_speak": "Text to be read aloud..."}
            ).model_dump()
        elif "navigate" in user_text:
            return NavigateResponse(
                data={"target_screen": "LIST_SCREEN"}
            ).model_dump()
        elif "show list" in user_text:
            return DisplayListResponse(
                data={
                    "material_list": [
                        {"id": "1", "title": "Material 1"},
                        {"id": "2", "title": "Material 2"}
                    ]
                }
            ).model_dump()
        elif "chapter" in user_text and current_context.active_material_id:
            # Example chapters for a selected material
            return DisplayChapterResponse(
                data={
                    "chapters": [
                        {"id": "1", "title": "Chapter 1: Introduction"},
                        {"id": "2", "title": "Chapter 2: Advanced Topics"}
                    ]
                }
            ).model_dump()
        elif "content" in user_text and current_context.active_chapter_id:
    # Example content for a selected chapter
            return DisplayContentResponse(
                data={
                    "material": {
                        "id": current_context.active_material_id,
                        "title": f"Chapter {current_context.active_chapter_id} Content",
                        "content": {
                            "text": "This is the content of the selected chapter.",
                            "images": [
                                {
                                    "url": "https://example.com/images/example.png",
                                    "description": "Example image"
                                }
                            ]
                        }
                    }
                }
            ).model_dump()
        else:
            return ErrorResponse(
                data={"error_message": "Unrecognized command or missing context."}
            ).model_dump()

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    
"""
Data example:
{
    "material": {
        "id": "1",
        "title": "Introduction to Python",
        "content": {
            "text": "Python is a versatile programming language used for web development, data analysis, artificial intelligence, and more [python_logo.png]. Python is first found on ...",
            "images": [
                {
                    "url": "https://example.com/images/python_logo.png",
                    "description": "Python logo"
                }
            ]
        }
    }
}

# Example of how to use the router in Postman
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