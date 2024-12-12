from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

#Engine is the way we can conect to the database
engine = create_engine('sqlite:///orm.db')

#creating the session wich is form interacting with the database

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#this is our taks model

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    title = Column(String(50))
    description = Column(String(100))
    status = Column(String(10))


Base.metadata.create_all(engine)

Task1 = Task(title='refactor the code',description='Refactor code for improved performance and readability.', status= 'In process.')
Task2 = Task(title='Optimize database queries', description='Improve database query efficiency.', status='In Progress')
Task3 = Task(title='Implement unit tests', description='Write unit tests to ensure code quality.', status='In Progress')
Task4 = Task(title='Upgrade dependencies', description='Update outdated libraries and frameworks.', status='In Progress')
Task5 = Task(title='Fix security vulnerabilities', description='Address identified security risks.', status='In Progress')
Task6 = Task(title='Improve code readability', description='Enhance code clarity and maintainability.', status='In Progress')
Task7 = Task(title='Deploy to production', description='Deploy the application to the production environment.', status='In Progress')
Task8 = Task(title='Integrate with external API', description='Connect the application to external services.', status='In Progress')
Task9 = Task(title='Implement user authentication', description='Add user authentication and authorization features.', status='In Progress')
Task10 = Task(title='Write technical documentation', description='Create documentation for developers and users.', status='In Progress')

#Creating the 'save' for saving the data

session.add_all([Task1,Task2,Task3,Task4,Task5,Task6,Task7,Task8,Task9,Task10])
session.commit()





