from sqlalchemy import Column, Integer, String, Float
from .database import Base

class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, index=True)
    label = Column(String, index=True)
    confidence = Column(Float)
    bbox_coordinates = Column(String)  # You might want to store this as JSON
