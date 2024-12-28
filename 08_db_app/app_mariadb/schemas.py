from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional


# 요청용 모델 (Create/Update)
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# 응답용 모델
# from_attributes = True: SQLAlchemy 모델 객체를 Pydantic 모델로 변환할 수 있도록 설정.
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
