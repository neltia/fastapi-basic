# app/services/user_service.py
# 사용자 비즈니스 로직을 수행하는 서비스
from sqlalchemy import select
from app.db.session import db_session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.config import settings
from app.core.security import PasswordManager  # 비밀번호 해시 함수


async def get_user_data(user_id: int):
    if settings.async_mode:
        async with db_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()
    else:
        with db_session() as session:
            return session.query(User).filter(User.id == user_id).first()


async def get_user_list(page: int, per_page: int):
    offset = (page - 1) * per_page
    if settings.async_mode:
        async with db_session() as session:
            result = await session.execute(
                select(User).offset(offset).limit(per_page)
            )
            users = result.scalars().all()
            total = await session.execute(select(User))
            total_count = total.scalars().all()
            return users, len(total_count)
    else:
        with db_session() as session:
            users = session.query(User).offset(offset).limit(per_page).all()
            total_count = session.query(User).count()
            return users, total_count


async def create_user(user: UserCreate):
    pw_hash = PasswordManager.hash_password(user.password)
    user_obj = User(
        username=user.username,
        email=user.email,
        password_hash=pw_hash,
        full_name=user.full_name,
        is_active=user.is_active
    )
    if settings.async_mode:
        async with db_session() as session:
            session.add(user_obj)
            await session.commit()
            await session.refresh(user_obj)
            return user_obj
    else:
        with db_session() as session:
            session.add(user_obj)
            session.commit()
            session.refresh(user_obj)
            return user_obj


async def update_user(user_id: int, user: UserUpdate):
    if settings.async_mode:
        async with db_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user_obj = result.scalars().first()
            if not user_obj:
                return None
            if user.username is not None:
                user_obj.username = user.username
            if user.email is not None:
                user_obj.email = user.email
            if user.full_name is not None:
                user_obj.full_name = user.full_name
            if user.is_active is not None:
                user_obj.is_active = user.is_active
            if user.password is not None:
                user_obj.password_hash = PasswordManager.hash_password(user.password)
            await session.commit()
            return user_obj
    else:
        with db_session() as session:
            user_obj = session.query(User).filter(User.id == user_id).first()
            if not user_obj:
                return None
            if user.username is not None:
                user_obj.username = user.username
            if user.email is not None:
                user_obj.email = user.email
            if user.full_name is not None:
                user_obj.full_name = user.full_name
            if user.is_active is not None:
                user_obj.is_active = user.is_active
            if user.password is not None:
                user_obj.password_hash = PasswordManager.hash_password(user.password)
            session.commit()
            return user_obj


async def delete_user(user_id: int):
    if settings.async_mode:
        async with db_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user_obj = result.scalars().first()
            if not user_obj:
                return False
            await session.delete(user_obj)
            await session.commit()
            return True
    else:
        with db_session() as session:
            user_obj = session.query(User).filter(User.id == user_id).first()
            if not user_obj:
                return False
            session.delete(user_obj)
            session.commit()
            return True
