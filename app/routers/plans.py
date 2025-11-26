from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/plans",
    tags=["plans"]
)


@router.post(
    "/", 
    response_model=schemas.PlanResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new membership plan"
)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    db_plan = models.Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get(
    "/", 
    response_model=List[schemas.PlanResponse],
    summary="Get all membership plans"
)
def get_plans(db: Session = Depends(get_db)):
    return db.query(models.Plan).all()
