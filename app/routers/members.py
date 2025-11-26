from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/members",
    tags=["members"]
)


@router.post(
    "/", 
    response_model=schemas.MemberResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new member"
)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
   
    existing_member = db.query(models.Member).filter(
        models.Member.phone == member.phone
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get(
    "/", 
    response_model=List[schemas.MemberResponse],
    summary="Get all members"
)
def get_members(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"), 
    db: Session = Depends(get_db)
):
    
    query = db.query(models.Member)

    if status_filter:
        query = query.filter(models.Member.status == status_filter)

    return query.all()


@router.get(
    "/{member_id}/current-subscription", 
    response_model=schemas.SubscriptionResponse,
    summary="Get member's current active subscription"
)
def get_current_subscription(member_id: int, db: Session = Depends(get_db)):
    
    member = db.query(models.Member).filter(
        models.Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    # Find active subscription
    now = datetime.now()
    subscription = db.query(models.Subscription).filter(
        models.Subscription.member_id == member_id,
        models.Subscription.start_date <= now,
        models.Subscription.end_date >= now
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found for this member"
        )

    return subscription


@router.get(
    "/{member_id}/attendance", 
    response_model=List[schemas.AttendanceResponse],
    summary="Get member's attendance history"
)
def get_member_attendance(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(
        models.Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    attendance = db.query(models.Attendance).filter(
        models.Attendance.member_id == member_id
    ).order_by(models.Attendance.check_in_time.desc()).all()

    return attendance
