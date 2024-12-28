from pydantic import BaseModel
from pydantic import StrictInt, ValidationError
from pydantic import Field
from pydantic import field_validator
from fastapi import FastAPI, Query, Path


app = FastAPI()


# StrictInt: 엄격한 타입 검증을 위해 사용, 문자열 같이 변환 가능해야 하는 값 비허용
class Product(BaseModel):
    name: str
    price: StrictInt  # Strict validation for integers


# Field 기반 검증
# - min_length, max_length: 문자열 길이 제한
# - ge, le: 숫자 최소/최대 값 설정
# - pattern: 정규식 이용 문자열 검증
class Employee(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., ge=18, le=65)  # Age between 18 and 65
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")


# field_validator decorator 기반 검증
class Event(BaseModel):
    name: str
    start_date: str
    end_date: str

    @field_validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:  # 종료일이 시작일보다 이전이면 오류 발생
            raise ValueError("end_date must be after start_date")
        return end_date


# In FastAPI, Path & Query 파라미터 검증
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., ge=1, le=1000),  # Path 파라미터 범위 검증, ...은 필수 값 명시
    q: str = Query(None, min_length=3, max_length=50)  # Query 파라미터 길이 제한
):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    # pydantic에서 검증 오류 시 ValidationError 오류 반환
    try:
        product = Product(name="Laptop", price="100")  # Raises ValidationError
    except ValidationError as e:
        print(e.json())

    employee = Employee(name="John Doe", age=30, email="john@example.com")
    print(employee.model_dump_json())
