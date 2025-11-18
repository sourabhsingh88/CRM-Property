# from sqlalchemy import Column, Integer, String, Text, LargeBinary
# from Backend.database import Base
#
#
# class Project(Base):
#     __tablename__ = "projects"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False)
#     description = Column(Text, nullable=False)
#     image = Column(LargeBinary)


# models/project_model.py
from sqlalchemy import Column, Integer, String
from Backend.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=True)   # store path, not bytes
