from sqlalchemy import Column, Integer, String, DateTime, Date, Enum, func, ForeignKey
from sqlalchemy.orm import relationship

from database.models import Base
from database.enums.task_enums import TaskStatus

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='tasks')
