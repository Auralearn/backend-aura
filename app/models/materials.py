from pydantic import BaseModel
from typing import Optional, List


class ChapterContent(BaseModel):
    text: str
    images: Optional[List[dict]] = []
    videos: Optional[List[dict]] = []
    audios: Optional[List[dict]] = []
    
class Chapter(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    content: List[ChapterContent]
    
class Material(BaseModel):
    id: str
    title: str
    chapters: List[Chapter]