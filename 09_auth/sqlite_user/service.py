from sqlalchemy.orm import Session
from sqlite_user.models import User
from sqlite_user.schemas import UserCreate
from fastapi import HTTPException
import bcrypt


# Hash a plaintext password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# Verify a plaintext password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserService:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        """사용자 인증 로직"""
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return {"message": "Login successful", "username": user.username}

    @staticmethod
    def list_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = hash_password(user.password)
        new_user = User(username=user.username, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    # 현재 비밀번호를 검증한 후 비밀번호를 변경
    @staticmethod
    def update_user(db: Session, username: str, current_password: str, new_password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 현재 비밀번호 검증
        if not verify_password(current_password, user.password):
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        # 새 비밀번호 해싱 후 저장
        user.password = hash_password(new_password)
        db.commit()
        return {"message": "Password updated successfully"}

    @staticmethod
    def delete_user(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
