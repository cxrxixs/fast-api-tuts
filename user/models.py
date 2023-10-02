from datetime import datetime

from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    blogs = relationship("Blog", back_populates="author")

    def __repr__(self) -> str:
        return f"{self.email}"
