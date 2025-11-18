from sqlalchemy import Column, Integer, String
from Backend.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(25), nullable=False)
    city = Column(String(255), nullable=False)


