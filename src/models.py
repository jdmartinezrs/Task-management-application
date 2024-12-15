from sqlalchemy import Column,Integer, String, Boolean,Sequence
from src.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,Sequence('task_id_seq'), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String,nullable=True)
    status = Column(Boolean,default=False,nullable=False)

    def __repr_(self):
        return f"<Task(id={self.id}, title={self.title},description={self.description}, status={self.status})>"
    

from sqlalchemy import Column, Integer, String, Boolean

