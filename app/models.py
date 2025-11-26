from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    join_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="active")
    total_check_ins = Column(Integer, default=0) 

    # Relationships
    subscriptions = relationship("Subscription", back_populates="member", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="member", cascade="all, delete-orphan")


class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plan.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    member = relationship("Member", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    check_in_time = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    member = relationship("Member", back_populates="attendance_records")
