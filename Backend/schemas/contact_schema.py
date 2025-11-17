from pydantic import BaseModel, EmailStr, constr

class ContactCreate(BaseModel):
    full_name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    mobile: constr(strip_whitespace=True, min_length=7, max_length=25)
    city: constr(strip_whitespace=True, min_length=1)

class ContactOut(BaseModel):
    id: int
    full_name: str
    email: str
    mobile: str
    city: str

    class Config:
        orm_mode = True
