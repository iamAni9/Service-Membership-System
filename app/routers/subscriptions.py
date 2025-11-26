from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)


@router.post(
    "/", 
    response_model=schemas.SubscriptionResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new subscription"
)
def create_subscription(
    subscription: schemas.SubscriptionCreate, 
    db: Session = Depends(get_db)
):
    member = db.query(models.Member).filter(
        models.Member.id == subscription.member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    plan = db.query(models.Plan).filter(
        models.Plan.id == subscription.plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    end_date = subscription.start_date + timedelta(days=plan.duration_days)

    db_subscription = models.Subscription(
        member_id=subscription.member_id,
        plan_id=subscription.plan_id,
        start_date=subscription.start_date,
        end_date=end_date
    )

    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription
