from sqlalchemy.orm import Session
from . import models, schemas

def get_results(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DetectionResult).offset(skip).limit(limit).all()

def create_result(db: Session, result: schemas.DetectionResultCreate):
    db_result = models.DetectionResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_result_by_id(db: Session, result_id: int):
    return db.query(models.DetectionResult).filter(models.DetectionResult.id == result_id).first()

def delete_result(db: Session, result_id: int):
    db_result = db.query(models.DetectionResult).filter(models.DetectionResult.id == result_id).first()
    if db_result:
        db.delete(db_result)
        db.commit()
    return db_result
