from pydantic import BaseModel

class TextSummaryResponse(BaseModel):
    text_id: str
    transcription: str
    summary: str