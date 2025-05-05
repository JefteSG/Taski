from models.task import Task
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_password import get_current_user
from models.user import User

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["tasks"]
)

@router.get("/", response_model=list[Task])
def get_tasks(db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Get all tasks.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    tasks = db.query(Task).all()
    return tasks

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Get a task by ID.
    """

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/user/{user_id}", response_model=list[Task])
def get_tasks_by_user(user_id: int, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Get tasks by user ID.
    """
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks

@router.post("/", response_model=Task)
def create_task(task: Task, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Create a new task.
    """
    # verificar o usuario tem superuser
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task.owner_id = current_user.id
    db.add(task)
    db.commit()
    db.refresh(task)
    return task 

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Update a task by ID.
    """
    # verificar o usuario tem superuser
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Delete a task by ID.
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return db_task
