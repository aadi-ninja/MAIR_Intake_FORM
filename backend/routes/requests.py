from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
import models
from schemas import RequestCreateSchema, RequestDetailSchema, RequestListSchema, StatusEnum
from datetime import datetime

router = APIRouter(prefix="/api/requests", tags=["Requests"])

# POST /api/requests - Create new request
@router.post("/", status_code=201)
def create_request(request: RequestCreateSchema, db: Session = Depends(get_db)):
    """Submit a new request"""
    try:
        # Create new request
        new_request = models.Request(
            title=request.title,
            description=request.description,
            request_type=request.request_type,
            business_unit=request.business_unit,
            priority=request.priority,
            submitted_by=request.submitted_by,
            status=StatusEnum.SUBMITTED
        )
        
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        
        # Log status change
        status_history = models.StatusHistory(
            request_id=new_request.id,
            old_status=None,
            new_status=StatusEnum.SUBMITTED,
            changed_by=request.submitted_by,
            changed_at=datetime.utcnow()
        )
        db.add(status_history)
        db.commit()
        
        # Return as dict
        return {
            "id": new_request.id,
            "title": new_request.title,
            "description": new_request.description,
            "request_type": new_request.request_type,
            "business_unit": new_request.business_unit,
            "priority": new_request.priority,
            "status": new_request.status,
            "submitted_by": new_request.submitted_by,
            "created_at": new_request.created_at,
            "updated_at": new_request.updated_at
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating request: {str(e)}")

# GET /api/requests - List requests
@router.get("/")
def list_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    user_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """List requests with optional filtering"""
    try:
        query = db.query(models.Request)
        
        # Filter by status if provided
        if status:
            query = query.filter(models.Request.status == status)
        
        # Filter by user if provided (for user's own requests)
        if user_id:
            query = query.filter(models.Request.submitted_by == user_id)
        
        # Order by most recent first
        requests = query.order_by(desc(models.Request.created_at)).offset(skip).limit(limit).all()
        
        # Convert to dicts
        return [
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "request_type": r.request_type,
                "status": r.status,
                "priority": r.priority,
                "created_at": r.created_at
            }
            for r in requests
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching requests: {str(e)}")

# GET /api/requests/{id} - Get request details
@router.get("/{request_id}")
def get_request_details(request_id: int, db: Session = Depends(get_db)):
    """Get detailed view of a specific request"""
    try:
        request = db.query(models.Request).filter(models.Request.id == request_id).first()
        
        if not request:
            raise HTTPException(status_code=404, detail=f"Request {request_id} not found")
        
        return {
            "id": request.id,
            "title": request.title,
            "description": request.description,
            "request_type": request.request_type,
            "business_unit": request.business_unit,
            "priority": request.priority,
            "status": request.status,
            "submitted_by": request.submitted_by,
            "created_at": request.created_at,
            "updated_at": request.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching request: {str(e)}")
