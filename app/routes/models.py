from typing import Optional, List, Dict
from pydantic import BaseModel

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

class MediaItem(BaseModel):
    url: str
    caption: str

class ContentBlock(BaseModel):
    text: str
    images: Optional[List[MediaItem]] = None
    videos: Optional[List[MediaItem]] = None

class ChapterContent(BaseModel):
    id: str
    title: str
    subtitle: str
    content: List[ContentBlock]

class DisplayContentData(BaseModel):
    material: ChapterContent

class DisplayContentResponse(BaseModel):
    action_type: str = "DISPLAY_CONTENT"
    data: DisplayContentData

class DisplayChapterResponse(BaseModel):
    action_type: str = "DISPLAY_CHAPTER"
    data: Dict[str, List[Dict[str, str]]]

class ErrorResponse(BaseModel):
    action_type: str = "ERROR"
    data: Dict[str, str]