from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Backend.models.contact_model import Contact
from Backend.database import SessionLocal

from Backend.schemas.contact_schema import ContactCreate, ContactOut

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# USER: submit contact form
@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    new_contact = Contact(
        full_name=payload.full_name,
        email=payload.email,
        mobile=payload.mobile,
        city=payload.city
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {"message": "Contact submitted successfully", "id": new_contact.id}


# ADMIN (or UI) view: get all contact submissions
@router.get("/", response_model=List[ContactOut])
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).order_by(Contact.id.desc()).all()
    return contacts


# Optional: single contact fetch
@router.get("/{contact_id}", response_model=ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
