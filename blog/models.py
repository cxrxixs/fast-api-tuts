from datetime import datetime

from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True)
    body = Column(String)
    created_at = Column(DateTime, server_default=func.as_utc())
    updated_at = Column(
        DateTime, server_default=func.as_utc(), onupdate=datetime.utcnow
    )
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")

    def __repr__(self) -> str:
        return f"{self.title}"
