from sqlalchemy import Column, Integer, String, Text, LargeBinary
from Backend.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # store image as bytes
