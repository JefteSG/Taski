from models.user import User
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_password import get_current_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Get a user by ID.
    """
    # validar token JWT
    # if not current_user:

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[User])
def get_users(db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Get all users.
    """
    users = db.query(User).all()
    return users


@router.post("/", response_model=User)
def create_user(user: User, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Create a new user.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: User, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Update a user by ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    """
    Delete a user by ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}



