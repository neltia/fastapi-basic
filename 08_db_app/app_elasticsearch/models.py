from pydantic import BaseModel, Field
from typing import List, Optional


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
    tags: List[str]


class ProductSearchQuery(BaseModel):
    query: Optional[str] = Field(None, example="Wireless Keyboard")
    category: Optional[str] = Field(None, example="Electronics")
    price_range: Optional[dict] = Field(
        None, example={"gte": 20.00, "lte": 50.00}
    )
    tags: Optional[List[str]] = Field(None, example=["wireless", "keyboard"])


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Keyboard Name")
    category: Optional[str] = Field(None, example="Updated Electronics")
    description: Optional[str] = Field(None, example="Updated description")
    price: Optional[float] = Field(None, example=24.99)
    tags: Optional[List[str]] = Field(None, example=["updated", "keyboard"])
