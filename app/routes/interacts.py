"""
TODO:
Create a route to handle the interaction with the Voice assistant.

Receives raw text (from Android STT), processes it to understand intent (navigation, content request, simple Q&A mockup), and returns instructions to the Android app.

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