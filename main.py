from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine, Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Engine is the way we connect to the database
engine = create_engine('sqlite:///orm.db')

# Creating the session which is for interacting with the database
Session = sessionmaker(bind=engine)

Base = declarative_base()

# This is our task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    title = Column(String(50))
    description = Column(String(100))
    status = Column(Boolean, default=False)


Base.metadata.create_all(engine)

# Creating task instances
Task1 = Task(title='Refactor the code', description='Refactor code for improved performance and readability.')
Task2 = Task(title='Optimize database queries', description='Improve database query efficiency.')

# Saving the tasks to the database
with Session() as session:  # Using context manager for automatic session closing
    session.add_all([Task1, Task2])
    session.commit()

# Fetch tasks by title
task = session.query(Task).filter_by(title='Refactor the code').first()
if task:
    print(task.title)
    print(task.description)
    print(task.status)
else:
    print("Task not found")

# Deleting a task by title
with Session() as session:
    task_to_delete = session.query(Task).filter_by(title='Write technical documentation').first()
    if task_to_delete:
        session.delete(task_to_delete)
        session.commit()
    else:
        print("Task not found for deletion")
