from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ...persistence.database import get_db
from ...persistence.models.user import User
from ...core.dependencies import verify_password, get_password_hash, create_access_token, get_current_user
from ...core.exceptions import AuthenticationException, ValidationException
from ...config import settings
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = settings.access_token_expire_minutes * 60

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    status: bool

@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    
    if existing_user:
        if existing_user.username == request.username:
            raise ValidationException(message="用户名已存在")
        else:
            raise ValidationException(message="邮箱已被注册")
    
    hashed_password = get_password_hash(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        full_name=request.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        status=new_user.status
    )

@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise AuthenticationException(message="用户名或密码错误")
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token)

@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(user: User = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        status=user.status
    )