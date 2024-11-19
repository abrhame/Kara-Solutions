from pydantic import BaseModel
from typing import Optional

class DetectionResultBase(BaseModel):
    image_path: str
    label: str
    confidence: float
    bbox_coordinates: str

class DetectionResultCreate(DetectionResultBase):
    pass

class DetectionResult(DetectionResultBase):
    id: int

    class Config:
        orm_mode = True
