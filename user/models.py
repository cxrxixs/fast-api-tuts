from datetime import datetime

from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import backref, relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.as_utc())
    updated_at = Column(
        DateTime, server_default=func.as_utc(), onupdate=datetime.utcnow
    )
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    blogs = relationship("Blog", back_populates="author")

    def __repr__(self) -> str:
        return f"{self.email}"
