from models import Task
from database import session

def create_task(title,description=None):
    new_task = Task(title=title,description=description)
    session.add(new_task)
    session.commit()
    return new_task

def get_all_tasks():
    return session.query(Task).all()

def get_task_by_id(task_id):
    return session.query(Task).filter_by(id=task_id).first()

def update_task(task_id, title=None,description =None, status=None):
    task = get_task_by_id(task_id)
    if not task:
        return None
    if title:
        task.title = title
    if description:
        task.description = description
    if status is not None:
        task.status = status
        session.commit()
        return task

def delete_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return None
    session.delete(task)
    session.commit()
    return task 
