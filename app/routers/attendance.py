from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"]
)


@router.post(
    "/check-in", 
    response_model=schemas.AttendanceResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Check in a member"
)
def check_in(
    check_in_data: schemas.AttendanceCheckIn, 
    db: Session = Depends(get_db)
):
  
    member = db.query(models.Member).filter(
        models.Member.id == check_in_data.member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    now = datetime.now()
    active_subscription = db.query(models.Subscription).filter(
        models.Subscription.member_id == check_in_data.member_id,
        models.Subscription.start_date <= now,
        models.Subscription.end_date >= now
    ).first()

    if not active_subscription:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No active subscription for this member"
        )

    attendance = models.Attendance(
        member_id=check_in_data.member_id,
        check_in_time=now
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

   
    return attendance
