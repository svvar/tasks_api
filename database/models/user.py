from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database.models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tasks = relationship('Task', back_populates='user')