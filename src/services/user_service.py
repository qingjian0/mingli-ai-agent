from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from ..persistence.models.user import User, UserProfile
from ..persistence.models.computation import ComputationRequest
from ..core.dependencies import get_password_hash, verify_password
from ..core.exceptions import ValidationException, NotFoundException, AuthenticationException
from ..persistence.database import get_db

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, username: str, email: str, password: str, full_name: Optional[str] = None) -> User:
        existing_user = self.db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                raise ValidationException(message="用户名已存在")
            else:
                raise ValidationException(message="邮箱已被注册")
        
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user
    
    def authenticate_user(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationException(message="用户名或密码错误")
        
        return user
    
    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException(message="用户不存在")
        return user
    
    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise NotFoundException(message="用户不存在")
        return user
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> User:
        user = self.get_user_by_id(user_id)
        
        if "username" in data:
            existing = self.db.query(User).filter(
                User.username == data["username"],
                User.id != user_id
            ).first()
            if existing:
                raise ValidationException(message="用户名已被使用")
            user.username = data["username"]
        
        if "email" in data:
            existing = self.db.query(User).filter(
                User.email == data["email"],
                User.id != user_id
            ).first()
            if existing:
                raise ValidationException(message="邮箱已被使用")
            user.email = data["email"]
        
        if "full_name" in data:
            user.full_name = data["full_name"]
        
        if "phone" in data:
            user.phone = data["phone"]
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        user.status = False
        self.db.commit()
    
    def get_user_computations(self, user_id: int, domain: Optional[str] = None, limit: int = 10) -> list:
        query = self.db.query(ComputationRequest).filter(ComputationRequest.user_id == user_id)
        
        if domain:
            query = query.filter(ComputationRequest.domain == domain)
        
        return query.order_by(ComputationRequest.created_at.desc()).limit(limit).all()