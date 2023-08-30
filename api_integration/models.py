from datetime import datetime

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    status = Column(Enum("RUNNING", "COMPLETED", "FAILED"), index=True, default="RUNNING")
    project_id = Column(String, index=True)
    project_name = Column(String, index=True)
    converted = Column(Boolean, default=False)

    created_at = Column(String, index=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String, index=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
