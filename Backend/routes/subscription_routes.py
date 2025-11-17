from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.models.subscription_model import Subscription
from Backend.schemas.subscription_schema import SubscribeRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_subscriber(payload: SubscribeRequest, db: Session = Depends(get_db)):
    email = payload.email

    existing = db.query(Subscription).filter(Subscription.email == email).first()
    if existing:
        return {"message": "Email already subscribed"}

    new_sub = Subscription(email=email)
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    return {"message": "Subscribed successfully", "id": new_sub.id}

@router.get("/")
def get_subscribers(db: Session = Depends(get_db)):
    return db.query(Subscription).order_by(Subscription.id.desc()).all()
