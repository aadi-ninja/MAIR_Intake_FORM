from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

# Enums
class RequestTypeEnum(str, enum.Enum):
    NEW_REQUEST = "NEW_REQUEST"
    CHANGE_REQUEST = "CHANGE_REQUEST"
    BUG_FIX = "BUG_FIX"

class StatusEnum(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_REVIEW = "IN_REVIEW"
    SENT_FOR_APPROVAL = "SENT_FOR_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(200))
    role = Column(String(50), nullable=False)  # admin, approver, user, developer
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submitted_requests = relationship("Request", back_populates="submitted_by_user")
    status_history = relationship("StatusHistory", back_populates="changed_by_user")
    comments = relationship("Comment", back_populates="user")
    approvals = relationship("Approval", back_populates="assigned_to_user")

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    request_type = Column(Enum(RequestTypeEnum), nullable=False)
    business_unit = Column(String(100))
    priority = Column(String(50))  # HIGH, MEDIUM, LOW
    status = Column(Enum(StatusEnum), default=StatusEnum.SUBMITTED)
    submitted_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submitted_by_user = relationship("User", back_populates="submitted_requests")
    attachments = relationship("Attachment", back_populates="request", cascade="all, delete-orphan")
    wsjf = relationship("WSJF", back_populates="request", uselist=False, cascade="all, delete-orphan")
    status_history = relationship("StatusHistory", back_populates="request", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="request", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="request", cascade="all, delete-orphan")

class Attachment(Base):
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255))
    file_path = Column(Text)
    uploaded_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    request = relationship("Request", back_populates="attachments")

class WSJF(Base):
    __tablename__ = "wsjf"
    
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), unique=True)
    user_business_value = Column(Integer)  # 1-9
    time_criticality = Column(Integer)  # 1-9
    risk_reduction = Column(Integer)  # 1-9
    job_size = Column(Integer)  # 1-9
    wsjf_score = Column(Numeric(10, 2))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    request = relationship("Request", back_populates="wsjf")

class StatusHistory(Base):
    __tablename__ = "status_history"
    
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(Enum(StatusEnum))
    new_status = Column(Enum(StatusEnum), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"))
    changed_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    request = relationship("Request", back_populates="status_history")
    changed_by_user = relationship("User", back_populates="status_history")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    request = relationship("Request", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Comment", remote_side=[id], backref="parent")

class Approval(Base):
    __tablename__ = "approvals"
    
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="PENDING")  # PENDING, APPROVED, REJECTED, MORE_INFO_REQUESTED
    feedback = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    request = relationship("Request", back_populates="approvals")
    assigned_to_user = relationship("User", back_populates="approvals")
