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

class DisplayContentResponse(BaseModel):
    action_type: str = "DISPLAY_CONTENT"
    data: Dict[str, Dict[str, str]]

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
        if "navigate" in user_text:
            return NavigateResponse(
                data={"target_screen": "LIST_SCREEN"}
            ).dict()
        elif "show list" in user_text:
            return DisplayListResponse(
                data={
                    "material_list": [
                        {"id": "1", "title": "Material 1"},
                        {"id": "2", "title": "Material 2"}
                    ]
                }
            ).dict()
        elif "content" in user_text:
            return DisplayContentResponse(
                data={
                    "material": {
                        "id": "1",
                        "title": "Material 1",
                        "content": "This is the content of Material 1."
                    }
                }
            ).dict()
        else:
            return ErrorResponse(
                data={"error_message": "Unrecognized command."}
            ).dict()

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))