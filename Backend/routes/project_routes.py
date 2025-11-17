from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from Backend.models.project_model import Project
from Backend.database import SessionLocal
import base64

print(">>> PROJECT ROUTES LOADED <<<")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    result = []

    for p in projects:
        if p.image:
            image_base64 = base64.b64encode(p.image).decode()
            image_url = f"data:image/png;base64,{image_base64}"
        else:
            image_url = None

        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "image": image_url
        })

    return result


# USER: Get all projects
# @router.get("/")
# def get_projects(db: Session = Depends(get_db)):
#     projects = db.query(Project).all()
#     result = []
#
#     for p in projects:
#         image_base64 = base64.b64encode(p.image).decode() if p.image else None
#         result.append({
#             "id": p.id,
#             "name": p.name,
#             "description": p.description,
#             "image": image_base64
#         })
#
#     return result

# ADMIN: Add project
@router.post("/add")
async def add_project(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = await image.read()

    new_project = Project(
        name=name,
        description=description,
        image=image_bytes
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project added successfully", "id": new_project.id}
