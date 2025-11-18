# from fastapi import APIRouter, Depends, UploadFile, File, Form
# from sqlalchemy.orm import Session
# from Backend.database import SessionLocal
# from Backend.models.client_model import Client
# import base64
#
# router = APIRouter()
#
#
# # ====================== DATABASE DEPENDENCY ======================
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# # ====================== USER API: GET CLIENTS ======================
#
# @router.get("/")
# def get_clients(db: Session = Depends(get_db)):
#     clients = db.query(Client).all()
#     result = []
#
#     for c in clients:
#         image_base64 = (
#             base64.b64encode(c.image).decode("utf-8")
#             if c.image else None
#         )
#
#         result.append({
#             "id": c.id,
#             "name": c.name,
#             "designation": c.designation,
#             "description": c.description,
#             "image": image_base64
#         })
#
#     return result
#
#
# # ====================== ADMIN API: ADD CLIENT ======================
#
# @router.post("/add")
# async def add_client(
#         name: str = Form(...),
#         designation: str = Form(...),
#         description: str = Form(...),
#         image: UploadFile = File(...),
#         db: Session = Depends(get_db)
# ):
#     image_bytes = await image.read()  # read file bytes
#
#     new_client = Client(
#         name=name,
#         designation=designation,
#         description=description,
#         image=image_bytes
#     )
#
#     db.add(new_client)
#     db.commit()
#     db.refresh(new_client)
#
#     return {
#         "message": "Client added successfully",
#         "id": new_client.id
#     }
#
#
# # ================== ADMIN API: GET ALL CLIENTS (RAW) ==================
#
# @router.get("/admin/all")
# def get_all_clients_admin(db: Session = Depends(get_db)):
#     clients = db.query(Client).all()
#     output = []
#
#     for c in clients:
#         output.append({
#             "id": c.id,
#             "name": c.name,
#             "designation": c.designation,
#             "description": c.description,
#             "image": None  # admin doesn’t need base64 (optional)
#         })
#
#     return output
#
#
#
# @router.delete("/delete/{id}")
# def delete_client(id: int, db: Session = Depends(get_db)):
#     row = db.query(Client).filter(Client.id == id).first()
#     db.delete(row)
#     db.commit()
#     return {"message": "Deleted"}


from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from Backend.database import SessionLocal
from Backend.models.client_model import Client
import os
from uuid import uuid4
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("uploads/clients")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ====================== USER API: GET CLIENTS ======================

@router.get("/")
def get_clients(request: Request, db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    result = []

    for c in clients:
        image_url = None
        if c.image:
            image_url = str(request.base_url).rstrip("/") + "/" + c.image

        result.append({
            "id": c.id,
            "name": c.name,
            "designation": c.designation,
            "description": c.description,
            "image": image_url
        })

    return result


# ====================== ADMIN API: ADD CLIENT ======================

@router.post("/add")
async def add_client(
        request: Request,
        name: str = Form(...),
        designation: str = Form(...),
        description: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # Create unique file name
    original = os.path.basename(image.filename)
    unique_name = f"{uuid4().hex}_{original}"
    file_path = f"uploads/clients/{unique_name}"
    full_path = UPLOAD_DIR / unique_name

    # Save file
    with open(full_path, "wb") as f:
        f.write(await image.read())

    # Save relative path in DB
    client = Client(
        name=name,
        designation=designation,
        description=description,
        image=file_path
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    image_url = str(request.base_url).rstrip("/") + "/" + file_path

    return {
        "message": "Client added successfully",
        "id": client.id,
        "image_url": image_url
    }


# ====================== ADMIN DELETE ======================

@router.delete("/delete/{id}")
def delete_client(id: int, db: Session = Depends(get_db)):
    row = db.query(Client).filter(Client.id == id).first()
    if row:
        # delete file
        if row.image and os.path.exists(row.image):
            try:
                os.remove(row.image)
            except:
                pass

        db.delete(row)
        db.commit()

    return {"message": "Deleted"}

#
