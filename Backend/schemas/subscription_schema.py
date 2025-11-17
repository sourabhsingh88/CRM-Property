from pydantic import BaseModel

class SubscribeRequest(BaseModel):
    email: str
