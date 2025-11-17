from fastapi import FastAPI
from Backend.database import Base, engine

# Import models (required so SQLAlchemy creates tables)
from  Backend.models.project_model import Project
from  Backend.models.client_model import Client
from  Backend.models.contact_model import Contact
from  Backend.models.subscription_model import Subscription

# Import routers
from  Backend.routes.project_routes import router as project_router
from  Backend.routes.client_routes import router as client_router
from  Backend.routes.contact_routes import router as contact_router
from  Backend.routes.subscription_routes import router as subscription_router

from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(project_router, prefix="/api/projects", tags=["Projects"])
app.include_router(client_router, prefix="/api/clients", tags=["Clients"])
app.include_router(contact_router, prefix="/api/contact", tags=["Contact"])
app.include_router(subscription_router, prefix="/api/subscribe", tags=["Subscription"])

@app.get("/")
def home():
    return {"message": "FastAPI backend running"}
