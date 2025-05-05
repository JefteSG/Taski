from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal
from auth.auth_password import create_access_token, verify_password, get_password_hash
from schemas.user import UserLogin, TokenResponse

router = APIRouter(
    prefix="/api/v1/login",
    tags=["login"]
)


@router.post("/", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.name == user.name).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = create_access_token(data={"sub": db_user.name})
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/register", response_model=User)
def register(user: User, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.hashed_password = get_password_hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user