from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    designation: str
    description: str
