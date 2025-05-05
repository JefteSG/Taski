from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from ..database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True, index=True)
    hashed_password = Column(String(250), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_last_login = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="owner")
