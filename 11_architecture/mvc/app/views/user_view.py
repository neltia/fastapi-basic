# app/views/user_view.py
# 서비스 결과를 Pydantic 응답 형식으로 변환하는 뷰
from typing import List
from app.schemas.user_schema import (
    UserResponse,
    UserListResponse,
    UserDeleteResponse
)


class UserView:
    @staticmethod
    def single(user) -> UserResponse:
        return UserResponse.model_validate(user)

    @staticmethod
    def list(users: List, total: int, page: int, per_page: int) -> UserListResponse:
        user_list = [UserResponse.model_validate(u) for u in users]
        return UserListResponse(users=user_list, total=total, page=page, per_page=per_page)

    @staticmethod
    def delete(user_id: int) -> UserDeleteResponse:
        return UserDeleteResponse(message="User deleted successfully", deleted_user_id=user_id)
