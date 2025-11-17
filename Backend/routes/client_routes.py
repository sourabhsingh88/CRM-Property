from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.models.client_model import Client
import base64

router = APIRouter()


# ====================== DATABASE DEPENDENCY ======================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ====================== USER API: GET CLIENTS ======================

@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    result = []

    for c in clients:
        image_base64 = (
            base64.b64encode(c.image).decode("utf-8")
            if c.image else None
        )

        result.append({
            "id": c.id,
            "name": c.name,
            "designation": c.designation,
            "description": c.description,
            "image": image_base64
        })

    return result


# ====================== ADMIN API: ADD CLIENT ======================

@router.post("/add")
async def add_client(
        name: str = Form(...),
        designation: str = Form(...),
        description: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    image_bytes = await image.read()  # read file bytes

    new_client = Client(
        name=name,
        designation=designation,
        description=description,
        image=image_bytes
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return {
        "message": "Client added successfully",
        "id": new_client.id
    }


# ================== ADMIN API: GET ALL CLIENTS (RAW) ==================

@router.get("/admin/all")
def get_all_clients_admin(db: Session = Depends(get_db)):
    return db.query(Client).all()
