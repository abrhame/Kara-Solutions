from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# API Endpoints
@app.post("/results/", response_model=schemas.DetectionResult)
def create_detection_result(result: schemas.DetectionResultCreate, db: Session = Depends(get_db)):
    return crud.create_result(db=db, result=result)

@app.get("/results/", response_model=list[schemas.DetectionResult])
def read_results(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_results(db=db, skip=skip, limit=limit)

@app.get("/results/{result_id}", response_model=schemas.DetectionResult)
def read_result(result_id: int, db: Session = Depends(get_db)):
    db_result = crud.get_result_by_id(db, result_id=result_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result

@app.delete("/results/{result_id}", response_model=schemas.DetectionResult)
def delete_result(result_id: int, db: Session = Depends(get_db)):
    db_result = crud.delete_result(db, result_id=result_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result
