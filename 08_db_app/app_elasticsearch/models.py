from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class ProductCreate(BaseModel):
    name: str = Field(..., example="Wireless Keyboard")
    category: str = Field(..., example="Electronics")
    description: Optional[str] = Field(None, example="A compact wireless keyboard")
    price: float = Field(..., example=29.99)
    tags: Optional[List[str]] = Field(default_factory=list, example=["keyboard", "wireless", "compact"])


class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str]
    price: float
    tags: List[str] = Field(default_factory=list)  # 기본값 빈 리스트 제공


class ProductSearchQuery(BaseModel):
    query: Optional[str] = Field(None, description="검색어")
    filters: Optional[Dict[str, str]] = Field(None, description="필터 조건 (e.g., {'category': 'electronics'})")
    sort_by: Optional[str] = Field(None, description="정렬 기준 필드 (e.g., 'price')")
    order: Optional[str] = Field(None, pattern="^(asc|desc)$", description="order by: 'asc' or 'desc'")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Keyboard Name")
    category: Optional[str] = Field(None, example="Updated Electronics")
    description: Optional[str] = Field(None, example="Updated description")
    price: Optional[float] = Field(None, example=24.99)
    tags: Optional[List[str]] = Field(None, example=["updated", "keyboard"])
